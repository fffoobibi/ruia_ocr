import re
from lxml.html import etree
from typing import Union
from ruia.field import RegexField


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

