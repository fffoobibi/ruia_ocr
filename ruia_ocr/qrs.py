import asyncio
import async_timeout

from typing import Callable, Optional
from inspect import iscoroutinefunction

from ruia import Spider
from ruia import Response
from ruia import Request

from ruia_ocr.service import BaseOcrService, RegionStr

__all__ = ['OcrResponse', 'OcrRequest', 'OcrSpider']


class OcrResponse(Response):
    def __init__(
        self,
        url: str,
        method: str,
        *,
        encoding: str = "",
        metadata: dict,
        cookies,
        history,
        headers: dict = None,
        status: int = -1,
        aws_json: Callable = None,
        aws_read: Callable = None,
        aws_text: Callable = None,
        uri: str = None,
        service: 'BaseOcrService' =None
    ):
        self._uri = uri
        self._service = service
        super(OcrResponse, self).__init__(
            url=self._service.service_url,
            method=method,
            encoding=encoding,
            metadata=metadata,
            cookies=cookies,
            history=history,
            headers=headers,
            status=status,
            aws_json=aws_json,
            aws_read=aws_read,
            aws_text=aws_text,
        )

    @property
    def uri(self):
        return self._uri

    @property
    def service(self):
        return self._service

    async def json(self, **kwargs):
        """Read and decodes JSON response."""
        res = await self._aws_json(**kwargs)
        return self._service.process_json(res)

    async def read(self, **kwargs):
        """Read response payload."""
        return await self._aws_read(**kwargs)

    async def text(self, **kwargs):
        """Read response payload and decode."""
        res = await self._aws_text(**kwargs)
        return self._service.process_text(res)

    def __str__(self):
        return f"<OcrResponse url[{self._method}]: {self._url} uri:{self._url}> status:{self._status}"


class OcrRequest(Request):
    def __init__(
        self,
        url: str,
        method: str = "GET",
        *,
        callback=None,
        encoding: Optional[str] = None,
        headers: dict = None,
        metadata: dict = None,
        request_config: dict = None,
        request_session=None,
        region: str = None,
        uri: str=None,
        service: 'BaseOcrService'=None,
        **kwargs,
    ):
        self.uri =  uri or url
        self.region = region
        self.service = service
        super(OcrRequest, self).__init__(
            self.service.service_url,
            method,
            callback=callback,
            encoding=encoding,
            headers=headers,
            metadata=metadata,
            request_config=request_config,
            request_session=request_session,
            **kwargs,
        )

    async def _make_request(self):
        """Make a request by using aiohttp"""
        self.logger.info(f"<{self.method}: {self.uri} {self.url}>")

        await self.service.request_process(self)

        if self.method == "GET":
            request_func = self.current_request_session.get(
                self.url,
                headers=self.headers,
                ssl=self.ssl,
                **self.aiohttp_kwargs)
        else:
            request_func = self.current_request_session.post(
                self.url,
                headers=self.headers,
                ssl=self.ssl,
                **self.aiohttp_kwargs)
        resp = await request_func
        return resp

    async def fetch(self, delay=True) -> OcrResponse:
        """Fetch all the information by using aiohttp"""

        if delay and self.request_config.get("DELAY", 0) > 0:
            await asyncio.sleep(self.request_config["DELAY"])

        timeout = self.request_config.get("TIMEOUT", 10)
        try:
            async with async_timeout.timeout(timeout):
                resp = await self._make_request()
            try:
                resp_encoding = resp.get_encoding()
            except:
                resp_encoding = self.encoding

            response = OcrResponse(uri=self.uri,
                                   service=self.service,
                                   url=str(resp.url),
                                   method=resp.method,
                                   encoding=resp_encoding,
                                   metadata=self.metadata,
                                   cookies=resp.cookies,
                                   headers=resp.headers,
                                   history=resp.history,
                                   status=resp.status,
                                   aws_json=resp.json,
                                   aws_text=resp.text,
                                   aws_read=resp.read)
            # Retry middleware
            aws_valid_response = self.request_config.get("VALID")
            if aws_valid_response and iscoroutinefunction(aws_valid_response):
                response = await aws_valid_response(response)
            if response.ok:
                return response
            else:
                return await self._retry(
                    error_msg=
                    f"Request url failed with status {response.status}!")
        except asyncio.TimeoutError:
            return await self._retry(error_msg="timeout")
        except Exception as e:
            return await self._retry(error_msg=e)
        finally:
            # Close client session
            if self.close_request_session:
                await self._close_request()

    def __repr__(self):
        return f"<{self.method} {self.uri} {self.url}>"


class OcrSpider(Spider):
    
   # ocr_service
    ocr_service: BaseOcrService = None

    # ocr_region:str  x1,y1,x2,y2;...
    # default: '' means  the whole picture to ocr
    # 1,1,0.5,0.5 means: cut from image 1,1, image.width * 0.5, image.height * 0.5
    # 1,1,200,200 means: cut from image 1,1,200,200 
    # 1,1,0.5,0.5;0.5,0.5,0.99,0.99 means: 
    #   cut from image 1,1,image.width * 0.5, image.height * 0.5 get image1  
    #   cut from image image.width * 0.5, image.height * 0.5 ,image.width * 0.99, image.height * 0.99  get image2
    #   stitching image1 image2 by row get new image to ocr
    ocr_region: RegionStr = ''

    def request(self,
                url: str,
                method: str = "GET",
                *,
                callback=None,
                encoding: Optional[str] = None,
                headers: dict = None,
                metadata: dict = None,
                request_config: dict = None,
                request_session=None,
                **kwargs):
        """Init a Request class for crawling html"""
        headers = headers or {}
        metadata = metadata or {}
        request_config = request_config or {}
        request_session = request_session or self.request_session

        headers.update(self.headers.copy())
        request_config.update(self.request_config.copy())
        self.ocr_service.ocr_options.update(region=self.ocr_region)
        uri = url
        p_url = self.ocr_service.service_url

        return OcrRequest(
                          p_url,
                          method,
                          callback=callback,
                          encoding=encoding,
                          headers=headers,
                          metadata=metadata,
                          request_config=request_config,
                          request_session=request_session,
                          region=self.ocr_region,
                          uri=url,
                          service=self.ocr_service,
                          **kwargs)
