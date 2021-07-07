import re
import os
import base64

from lxml.html import etree

from ruia_ocr.service import BaseOcrService
from ruia_ocr.qrs import OcrRequest

from typing import Any, Union

from ruia.field import RegexField
from ruia.item import Item

from PIL import Image
from io import BytesIO



__all__ = ['OcrField']


class OcrField(RegexField):
    '''
    Inherited from RegexField, The OcrField is exactly the same with RegexField
    '''
    def __init__(self,
                 re_select: str,
                 re_flags=re.DOTALL | re.S,
                 default="ResultNotFound",
                 many: bool = False):
        super().__init__(re_select, re_flags, default, many)

    def extract(self, html: Union[str, etree._Element]):
        if isinstance(html, etree._Element):
            html = etree.tostring(html, encoding='utf8').decode()
            try:
                res = re.findall(r'<html><body><p>(.*)</p></body></html>',
                                 html,
                                 flags=re.DOTALL | re.S)
                html = res[0]
            except:
                pass
        if self.many:
            matches = self._re_object.finditer(html)
            return [self._parse_match(match) for match in matches]
        else:
            match = self._re_object.search(html)
            return self._parse_match(match)


# class ROcrItem(Item):

#     @classmethod
#     def set_ocr_sev(cls, ocr_serve: BaseOcrService):
#         if getattr(cls, 'ocr_serve', None) is None:
#             cls.ocr_serve = ocr_serve

#     @classmethod
#     async def get_item(
#         cls,
#         *,
#         html: str = "",
#         url: str = "",
#         html_etree: etree._Element = None,
#         service: BaseOcrService = None,
#         **kwargs,
#     ) -> Any:
#         if url:
#             if service is None:
#                 raise ValueError('<ROcrItem: url *and* service both expected.')
#         if service:
#             cls.set_ocr_sev(service)
#         return await super().get_item(html=html,
#                                       url=url,
#                                       html_etree=html_etree,
#                                       **kwargs)

#     @classmethod
#     async def get_items(cls, *, html: str, url: str,
#                         html_etree: etree._Element, **kwargs):
#         return

#     @classmethod
#     def _process_image(cls, image: Image.Image, region: 'RegionStr'):
#         # Stitching pictures
#         if region:
#             boxs = []
#             for v in region.strip(';').split(';'):
#                 box = list((map(float, v.split(','))))
#                 for index, coord in enumerate(box):
#                     if index % 2 == 0:
#                         box[index] = image.width * coord if coord < 1 else coord
#                     else:
#                         box[index] = image.height * coord if coord < 1 else coord
#                 box = tuple(map(int, box))
#                 boxs.append(box)
#             imgs = [image.crop(box) for box in boxs]
#             width, height = list(zip(*[img.size for img in imgs]))
#             max_width = max(width)
#             img_new = Image.new('RGB', (max_width, sum(height)))
#             for index, img in enumerate(imgs):
#                 box = (0, sum(height[:index]), img.width,
#                        sum(height[:index + 1]))
#                 img_new.paste(img, box)
#             return img_new
#         else:
#             return image

#     @classmethod
#     def _adapter_request(cls, request, image: str):
#         if hasattr(cls, 'ocr_serve'):
#             serve = cls.ocr_serve
#             if serve:
#                 if not hasattr(request, '_middle_processed'):
#                     payloads = serve._service_payload.copy()
#                     request.metadata = {'image': os.path.basename(request.url)}
#                     request.ocr_url = request.url
#                     request.url = serve.service_url
#                     request.method = 'POST'
#                     request.headers = serve._headers
#                     aiohttp_kwargs = request.aiohttp_kwargs
#                     aiohttp_kwargs.pop('params', None)
#                     aiohttp_kwargs.pop('data', None)
#                     aiohttp_kwargs.update(params=serve._params)
#                     region = serve.ocr_options.get('region')
#                     _image = Image.open(image)
#                     _image = cls._process_image(_image, region)
#                     image_io = BytesIO()
#                     _image.save(image_io, format='PNG')
#                     image_data = base64.b64encode(image_io.getvalue()).decode()
#                     payloads.update(image=image_data)
#                     aiohttp_kwargs.update(data=payloads)
#                     request.aiohttp_kwargs = aiohttp_kwargs

#     @classmethod
#     async def _get_html(cls, html: str = "", url: str = "", **kwargs):
#         if html and url:
#             raise ValueError("<ROcrItem: html *or* url expected, not both.")
#         if html or url:
#             if url:
#                 sem = kwargs.pop("sem", None)
#                 # request = Request(url, **kwargs)
#                 request = OcrRequest(url, **kwargs)
#                 # cls._adapter_request(request, url)
#                 if sem:
#                     _, response = await request.fetch_callback(sem=sem)
#                 else:
#                     response = await request.fetch()
#                 html = await cls.html_to_needed(response)
#             return html
#         else:
#             raise ValueError("<ROcrItem: html(url or html_etree) is expected.")


#     @classmethod
#     async def html_to_needed(cls, response):
#         if hasattr(cls, 'ocr_serve'):
#             return await cls.ocr_serve.html_to_plain(response)

#     def __repr__(self):
#         return f"<ROcrItem {self.results}>"
