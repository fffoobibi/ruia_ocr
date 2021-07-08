import os
import base64
import hmac
import hashlib
import datetime
import aiohttp
import requests
import json

from PIL import Image
from io import BytesIO
from urllib.parse import urlparse, quote, urlencode
from typing import Any, List, Tuple, Union
from enum import Enum

from ruia import Request
from ruia.utils import get_logger
from ruia_ocr.exceptions import ServicePayloadsError, ImageTypeError
from ruia_ocr.configs import *

logger = get_logger('Spider')

_Number = Union[int, float]

Region = Tuple[_Number, _Number, _Number, _Number] # (x1, y1, x2, y2)

RegionStr = str #  x1,y1,x2,y2;...  example 1,1,200,200;1,1,0.9,0.9

try:
    # Adaptive interface changes. It's recommended to do this
    from aip.base import AipBase

    _access_token_url = AipBase._AipBase__accessTokenUrl
except:
    # Fixed api implementation, not recommended
    _access_token_url = 'https://aip.baidubce.com/oauth/2.0/token'



__all__ = ['BaiduOcrService', 'BaseOcrService']


def getAuthrHeaders(method,
                    url,
                    params=None,
                    headers=None,
                    _apiKey=None,
                    _secretKey=None):
    headers = headers or {}
    params = params or {}

    urlResult = urlparse(url)
    for kv in urlResult.query.strip().split('&'):
        if kv:
            k, v = kv.split('=')
            params[k] = v

    # UTC timestamp
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    headers['Host'] = urlResult.hostname
    headers['x-bce-date'] = timestamp
    version, expire = '1', '1800'

    # 1 Generate SigningKey
    val = "bce-auth-v%s/%s/%s/%s" % (version, _apiKey, timestamp, expire)
    signingKey = hmac.new(_secretKey.encode('utf-8'), val.encode('utf-8'),
                          hashlib.sha256).hexdigest()

    # 2 Generate CanonicalRequest
    # 2.1 Genrate CanonicalURI
    canonicalUri = quote(urlResult.path)
    # 2.2 Generate CanonicalURI: not used here
    # 2.3 Generate CanonicalHeaders: only include host here

    canonicalHeaders = []
    for header, val in headers.items():
        canonicalHeaders.append(
            '%s:%s' %
            (quote(header.strip(), '').lower(), quote(val.strip(), '')))
    canonicalHeaders = '\n'.join(sorted(canonicalHeaders))

    # 2.4 Generate CanonicalRequest
    canonicalRequest = '%s\n%s\n%s\n%s' % (
        method.upper(), canonicalUri, '&'.join(
            sorted(urlencode(params).split('&'))), canonicalHeaders)

    # 3 Generate Final Signature
    signature = hmac.new(signingKey.encode('utf-8'),
                         canonicalRequest.encode('utf-8'),
                         hashlib.sha256).hexdigest()

    headers['authorization'] = 'bce-auth-v%s/%s/%s/%s/%s/%s' % (
        version, _apiKey, timestamp, expire, ';'.join(
            headers.keys()).lower(), signature)

    return headers


class BaseOcrService(object):
    '''
    You can implement your own ocr-services by only implementing a subclass.
    Service url and service type and service data are one-to-one corresponding
    You can rewrite both methods to customize your own ocr-service
    name: ocr-service 's name
    service_types: This is a list(List[str]) of all service types that contain the interfaces defined by you, and you should implement it in a subclass
    '''

    name = 'BaseOcrService'

    service_types = None

    def __init__(self):
        self._service_url: str = None
        self._service_type: BaseServiceTypes = None
        self._service_payload = None
        self._ocr_options = {}

    def __repr__(self):
        return f'{self.name}<{self.service_url}, {self.service_type}>'

    @property
    def ocr_options(self):
        return self._ocr_options

    @ocr_options.setter
    def ocr_options(self, value):
        self._ocr_options = value

    def set_payload(self, payloads: Any) -> None:
        '''
        :param payloads: The parameters of the service you requested,is a python dict

        dft:
            payload = self._service_type.dft_payload.copy()
            payload.update(payloads)
            self._service_payload = payloads

        '''
        return NotImplemented
     
    register_payload = set_payload

    def update_dft_payload(self, payloads) -> None:
        self._service_type.update_dft_payload(payloads)

    @property
    def service_url(self):
        '''
        :return:  Return the servicse url of your task requirements
        '''
        if self._service_url is None:
            self._service_url = self._service_type.url
        return self._service_url

    @property
    def service_type(self):
        '''
        :return:  Return your service type
        '''
        return self._service_type

    @property
    def service_payload(self):
        '''
        :return: Return the parameters that your service needs to send
        '''
        return self._service_payload

    async def aio_request(self, image_path: str, region: RegionStr=None, *, img: Image.Image=None) -> dict:
        return NotImplemented
        
    def request(self, image_path: str=None, region: RegionStr=None, *, img: Image.Image=None) -> dict:
        return NotImplemented

    def _process_region(self, image: Image.Image, region: RegionStr) -> List[Region]:
        '''
        region: 1,1,200,200 or 1,1, 0.9, 0.9
        '''
        boxs = []
        for v in region.strip(';').split(';'):
            box = list((map(float, v.split(','))))
            for index, coord in enumerate(box):
                if index % 2 == 0:
                    box[index] = image.width * coord if coord < 1 else coord
                else:
                    box[index] = image.height * coord if coord < 1 else coord
                    
            box = tuple(map(int, box))
            boxs.append(box)
        return boxs

    def _get_image_by_region(self, image: Image.Image, region: RegionStr=None) -> Image.Image:
        if region:
            # Stitching pictures
            boxs = self._process_region(image, region)
            imgs = [image.crop(box) for box in boxs]
            width, height = list(zip(*[img.size for img in imgs]))
            max_width = max(width)
            img_new = Image.new('RGB', (max_width, sum(height)))
            for index, img in enumerate(imgs):
                box = (0, sum(height[:index]), img.width,
                       sum(height[:index + 1]))
                img_new.paste(img, box)
            # img_new.show()
            return img_new
        else:
            return image

    def get_ocr_image(self, file_path: str, request, region: RegionStr=None) -> Any:
        '''
        Converting the local-image to be detected becomes the data that Ocr api eventually sends
        '''
        _image = Image.open(file_path)
        _image = self._get_image_by_region(_image, region)
        return self.image_convert_ocr(_image, request)

    async def request_process(self, request: Request, spider_ins=None):
        '''
        Modify the Request parameters. Transform interface parameters to implement Ocr api
        '''
        raise NotImplementedError

    def process_text(self, text: str):
        '''
        Hook function: process await response.text()
        '''
        return text

    def process_json(self, json: dict):
        '''
        Hook function: process await response.json()
        '''
        return json

    def image_convert_ocr(self, image: Image.Image, request) -> Any:
        '''
        Hook function: Converting the local-image to be detected becomes the data that Ocr api eventually sends
        '''
        raise NotImplementedError


class BaiDuOcrResult(str, Enum):
    BY_ROW = '\n'
    JOIN = ''


class BaiduOcrService(BaseOcrService):
    '''
    Built-in configuration parameters for 2 services, GENERALBASIC and GENERAL.
    If you need to use baidu-ocr extra services, configure the parameters to match by use method update_dft_payload

    '''
    name = "Baidu-Ocr"

    service_types = list(BaiDuServiceTypes.__members__.keys())

    access_token_url = _access_token_url

    def __init__(self,
                 app_id,
                 api_key,
                 secret_key,
                 service_type: BaiDuServiceTypes=BaiDuServiceTypes.BAIDU_GENERALBASIC_TYPE,
                 sep: BaiDuOcrResult=BaiDuOcrResult.JOIN):
        '''
        :param app_id: your app_id, See more at https://ai.baidu.com/docs#/OCR-API/top
        :param api_key: your api_key, See more at https://ai.baidu.com/docs#/OCR-API/top
        :param secret_key: your secret_key, See more at https://ai.baidu.com/docs#/OCR-API/top
        :param service_type: your request service type, There are a total of 41 service types,
        See more at https://ai.baidu.com/docs#/OCR-API/top
        '''

        super().__init__()
        self.app_id = app_id
        self.api_key = api_key
        self.sep = sep
        self.secret_key = secret_key
        self._service_type = service_type
        self._service_url = None
        self._service_payload = service_type.dft_payload
        self._ocr_options = {}
        if service_type.value not in self.service_types:
            raise ServicePayloadsError(
                'Baidu-Ocr service must in %s \n See more details at '
                'https://ai.baidu.com/docs#/OCR-API/top' % self.service_types)

        try:
            # Adaptive interface changes. It's recommended to do this
            from aip import AipOcr
            _ocr = AipOcr(app_id, api_key, secret_key)
            _authobj = _ocr._auth()
            _version = _ocr.getVersion()
            self._access_token = _ocr._auth().get('access_token')
            self._params = _ocr._getParams(_authobj)
            self._params.update(aipSdk='python', aipVersion=_version)
        except:
            # Fixed api implementation, not recommended
            self._access_token = None
            self._params = {
                'access_token': self._access_token,
                'aipSdk': 'python'
            }
        finally:
            self._access_token_semphone = None
            headers = getAuthrHeaders('POST',
                                      self.service_url,
                                      _apiKey=self.api_key,
                                      _secretKey=self.secret_key)
            headers.update(
                {'Content-Type': 'application/x-www-form-urlencoded'})
            self._headers = headers

    async def _get_access_token(self):
        '''
        baidu-ocr service need access_token, this method try to get this parameter.
        :return: access_token
        '''
        if self._access_token is None:
            response = await Request(url=self.access_token_url,
                                     params={
                                         'grant_type': 'client_credentials',
                                         'client_id': self.api_key,
                                         'client_secret': self.secret_key
                                     }).fetch()
            json = await response.json()
            self._access_token, self._expires_in = json.get(
                'access_token'), json.get('expires_in')
        return self._access_token

    def set_payload(self, payloads: dict) -> None:
        payload = self._service_type.dft_payload.copy()
        payload.update(payloads)
        self._service_payload = payloads

    def image_convert_ocr(self, _image: Image.Image, request) -> Any:
        _max = max(_image.height, _image.width)
        _min = min(_image.height, _image.width)
        if _max > 4096:
            request.retry_times = 0
            logger.error(
                'Baidu-ocr \'s longest edge of the picture can not exceed 4096 px'
            )
            raise ImageTypeError
        if _min < 15:
            request.retry_times = 0
            logger.error(
                'Baidu-ocr \'s shortest edge of the picture cannot be less than 15 px'
            )
            raise ImageTypeError
        image_io = BytesIO()
        _image.save(image_io, format='PNG')
        return base64.b64encode(image_io.getvalue()).decode()

    async def _localImage_or_webImage_parse(self, request: Request,
                                            spider_ins=None):
        '''
        process image-data(loacl-image or web-image) update baidu pay_loads
        :param request: Request
        '''
        _raw_url = request.uri
        if _raw_url.startswith('https'):
            logger.error('Baidu-ocr does not support remote https image link,'
                         'check your start_urls')
            request.retry_times = 0
            raise ImageTypeError
        elif _raw_url.startswith('http'):
            # self._service_payload.update(url=_raw_url)
            self._service_payload.pop('image', None)
            self._service_payload.update(url=_raw_url)
        else:
            if _raw_url[-3:].lower() not in ['jpg', 'png', 'bmp', 'peg']:
                logger.error('Baidu does not support this type of picture , '
                             'must be `jpg`, `png`, `bmp` or `jpeg`')
                request.retry_times = 0
                request._ok = False
                raise ImageTypeError
            else:
                image = self.get_ocr_image(
                    _raw_url,
                    request,
                    region=self.ocr_options.get('region', None))
                self._service_payload.pop('url', None)
                self._service_payload.update(image=image)

    async def request_process(self, request: 'OcrRequest', spider_ins=None):
        # Baidu ocr's request header parameters
        # headers = getAuthrHeaders('POST', self.service_url, _apiKey=self.api_key,
        #                           _secretKey=self.secret_key)
        # headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        await self._localImage_or_webImage_parse(request, spider_ins)
        pay_loads = self._service_payload.copy()
        request.metadata = {'image': os.path.basename(request.url)}
        request.uri = request.url
        request.url = self.service_url
        request.method = 'POST'
        request.headers = self._headers
        aiohttp_kwargs = request.aiohttp_kwargs
        aiohttp_kwargs.pop('params', None)
        aiohttp_kwargs.pop('data', None)
        aiohttp_kwargs.update(params=self._params)
        aiohttp_kwargs.update(data=pay_loads)
        request.aiohttp_kwargs = aiohttp_kwargs
        request._middle_processed = True # 已处理标志位

    def process_text(self, text: str):
        jsons = json.loads(text)
        return self.process_json(jsons)

    def process_json(self, json: dict):
        words_result = json.get('words_result', None)
        res = []
        if isinstance(words_result, list):
            if words_result:
                for dic in words_result:
                    res.append(dic.get('words'))
                return self.sep.join(res)
        return ''

    async def aio_request(self, image_path: str, region: RegionStr=None, *, img: Image.Image=None):
        if img is None:
            if image_path[-3:].lower() not in ['jpg', 'png', 'bmp', 'peg']:
                logger.error('Baidu does not support this type of picture , '
                            'must be `jpg`, `png`, `bmp` or `jpeg`')
                raise ImageTypeError
            image = Image.open(image_path)
        else:
            image = img

        if region:
            image = self._get_image_by_region(image, region)

        image_io = BytesIO()
        image.save(image_io, format='PNG')
        b64_data = base64.b64encode(image_io.getvalue()).decode()
        payloads = self.service_payload.copy()
        payloads.update({'image': b64_data})

        async with aiohttp.request('POST',
                             url=self.service_url,
                             headers=self._headers,
                             params=self._params,
                             data=payloads) as r:
            return await r.json()
        
    def request(self, image_path: str=None, region: RegionStr=None, *, img: Image.Image=None):
        if img is None:
            if image_path[-3:].lower() not in ['jpg', 'png', 'bmp', 'peg']:
                logger.error('Baidu does not support this type of picture , '
                            'must be `jpg`, `png`, `bmp` or `jpeg`')
                raise ImageTypeError
            image = Image.open(image_path)
        else:
            image = img

        if region:
            image = self._get_image_by_region(image, region)
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        b64_data = base64.b64encode(image_io.getvalue()).decode()
        payloads = self.service_payload.copy()
        payloads.update({'image': b64_data})
        json = requests.post(url=self.service_url,
                             headers=self._headers,
                             params=self._params,
                             data=payloads).json()
        return json

