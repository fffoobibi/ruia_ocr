# This module defines the basic parameters of Baidu ocr service
from enum import Enum
from aip import AipOcr

__all__ = ['BaseServiceTypes', 'BaiDuServiceTypes']

class BaseServiceTypes(str, Enum):

    @property
    def dft_payload(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    def update_dft_payload(self, value):
        return NotImplemented

def _get_baidu_services_configs():
    for key, value in AipOcr.__dict__.items():
        if isinstance(value, str) and key.startswith('_AipOcr'):
            _ = key[9:].upper().strip('URL')
            _key_url = f'BAIDU_{_}_URL'
            _key_type = f'BAIDU_{_}_TYPE'
            _key_payload = f'BAIDU_{_}_PAYLOAD'
            pay_load = {}
            if _key_url == 'BAIDU_GENERALBASIC_URL':
                pay_load["language_type"] = "CHN_ENG"
                pay_load["detect_direction"] = "true"
                pay_load["detect_language"] = "true"
                pay_load["probability"] = "true"
            elif _key_url == 'BAIDU_GENERAL_URL':
                pay_load["language_type"] = "CHN_ENG"
                pay_load["detect_direction"] = "true"
                pay_load["detect_language"] = "true"
                pay_load["probability"] = "true"
            baidu_ocr_types[_key_type] = _key_type
            baidu_ocr_services_configs[_key_type] = {
                'url': value,
                'pay_load': pay_load.copy()
            }

baidu_ocr_services_configs = {}

baidu_ocr_types = {}

_get_baidu_services_configs()

class BaiDuServiceTypes(BaseServiceTypes):
        BAIDU_GENERALBASIC_TYPE = "BAIDU_GENERALBASIC_TYPE"
        BAIDU_ACCURATEBASIC_TYPE = "BAIDU_ACCURATEBASIC_TYPE"
        BAIDU_GENERA_TYPE = "BAIDU_GENERA_TYPE"
        BAIDU_ACCURATE_TYPE = "BAIDU_ACCURATE_TYPE"
        BAIDU_GENERALENHANCED_TYPE = "BAIDU_GENERALENHANCED_TYPE"
        BAIDU_WEBIMAGE_TYPE = "BAIDU_WEBIMAGE_TYPE"
        BAIDU_IDCARD_TYPE = "BAIDU_IDCARD_TYPE"
        BAIDU_BANKCARD_TYPE = "BAIDU_BANKCARD_TYPE"
        BAIDU_DRIVINGLICENSE_TYPE = "BAIDU_DRIVINGLICENSE_TYPE"
        BAIDU_VEHICLELICENSE_TYPE = "BAIDU_VEHICLELICENSE_TYPE"
        BAIDU_ICENSEPLATE_TYPE = "BAIDU_ICENSEPLATE_TYPE"
        BAIDU_BUSINESSLICENSE_TYPE = "BAIDU_BUSINESSLICENSE_TYPE"
        BAIDU_ECEIPT_TYPE = "BAIDU_ECEIPT_TYPE"
        BAIDU_TRAINTICKET_TYPE = "BAIDU_TRAINTICKET_TYPE"
        BAIDU_TAXIRECEIPT_TYPE = "BAIDU_TAXIRECEIPT_TYPE"
        BAIDU_FORM_TYPE = "BAIDU_FORM_TYPE"
        BAIDU_TABLERECOGNIZE_TYPE = "BAIDU_TABLERECOGNIZE_TYPE"
        BAIDU_TABLERESULTGET_TYPE = "BAIDU_TABLERESULTGET_TYPE"
        BAIDU_VINCODE_TYPE = "BAIDU_VINCODE_TYPE"
        BAIDU_QUOTAINVOICE_TYPE = "BAIDU_QUOTAINVOICE_TYPE"
        BAIDU_HOUSEHOLDREGISTE_TYPE = "BAIDU_HOUSEHOLDREGISTE_TYPE"
        BAIDU_HKMACAUEXITENTRYPERMIT_TYPE = "BAIDU_HKMACAUEXITENTRYPERMIT_TYPE"
        BAIDU_TAIWANEXITENTRYPERMIT_TYPE = "BAIDU_TAIWANEXITENTRYPERMIT_TYPE"
        BAIDU_BIRTHCERTIFICATE_TYPE = "BAIDU_BIRTHCERTIFICATE_TYPE"
        BAIDU_VEHICLEINVOICE_TYPE = "BAIDU_VEHICLEINVOICE_TYPE"
        BAIDU_VEHICLECERTIFICATE_TYPE = "BAIDU_VEHICLECERTIFICATE_TYPE"
        BAIDU_INVOICE_TYPE = "BAIDU_INVOICE_TYPE"
        BAIDU_AIRTICKET_TYPE = "BAIDU_AIRTICKET_TYPE"
        BAIDU_INSURANCEDOCUMENTS_TYPE = "BAIDU_INSURANCEDOCUMENTS_TYPE"
        BAIDU_VATINVOICE_TYPE = "BAIDU_VATINVOICE_TYPE"
        BAIDU_QRCODE_TYPE = "BAIDU_QRCODE_TYPE"
        BAIDU_NUMBERS_TYPE = "BAIDU_NUMBERS_TYPE"
        BAIDU_OTTERY_TYPE = "BAIDU_OTTERY_TYPE"
        BAIDU_PASSPORT_TYPE = "BAIDU_PASSPORT_TYPE"
        BAIDU_BUSINESSCARD_TYPE = "BAIDU_BUSINESSCARD_TYPE"
        BAIDU_HANDWRITING_TYPE = "BAIDU_HANDWRITING_TYPE"
        BAIDU_CUSTOM_TYPE = "BAIDU_CUSTOM_TYPE"

        @property
        def dft_payload(self) -> dict:
            config = baidu_ocr_services_configs.get(self, None)
            if config:
                return config.get('pay_load', {}).copy()
            return {}

        @property
        def url(self) -> str:
            config = baidu_ocr_services_configs.get(self, None)
            if config:
                return config.get('url', '')
            return ''

        def update_dft_payload(self, value: dict):
            config = baidu_ocr_services_configs.get(self)
            if config:
                config['pay_load'].update(value)