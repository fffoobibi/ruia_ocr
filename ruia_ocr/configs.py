# This module defines the basic parameters of Baidu ocr service
from ruia.utils import get_logger

__all__ = ['baidu_ocr_urls', 'baidu_ocr_payloads', 'baidu_ocr_types',
           'register_baidu_service',
           "BAIDU_GENERALBASIC_TYPE", "BAIDU_ACCURATEBASIC_TYPE", "BAIDU_GENERAL_TYPE", "BAIDU_ACCURATE_TYPE",
           "BAIDU_GENERALENHANCED_TYPE", "BAIDU_WEBIMAGE_TYPE", "BAIDU_IDCARD_TYPE", "BAIDU_BANKCARD_TYPE",
           "BAIDU_DRIVINGLICENSE_TYPE", "BAIDU_VEHICLELICENSE_TYPE", "BAIDU_LICENSEPLATE_TYPE",
           "BAIDU_BUSINESSLICENSE_TYPE", "BAIDU_RECEIPT_TYPE", "BAIDU_TRAINTICKET_TYPE", "BAIDU_TAXIRECEIPT_TYPE",
           "BAIDU_FORM_TYPE", "BAIDU_TABLERECOGNIZE_TYPE", "BAIDU_TABLERESULTGET_TYPE", "BAIDU_VINCODE_TYPE",
           "BAIDU_QUOTAINVOICE_TYPE", "BAIDU_HOUSEHOLDREGISTER_TYPE", "BAIDU_HKMACAUEXITENTRYPERMIT_TYPE",
           "BAIDU_TAIWANEXITENTRYPERMIT_TYPE", "BAIDU_BIRTHCERTIFICATE_TYPE", "BAIDU_VEHICLEINVOICE_TYPE",
           "BAIDU_VEHICLECERTIFICATE_TYPE", "BAIDU_INVOICE_TYPE", "BAIDU_AIRTICKET_TYPE",
           "BAIDU_INSURANCEDOCUMENTS_TYPE", "BAIDU_VATINVOICE_TYPE", "BAIDU_QRCODE_TYPE", "BAIDU_NUMBERS_TYPE",
           "BAIDU_LOTTERY_TYPE", "BAIDU_PASSPORT_TYPE", "BAIDU_BUSINESSCARD_TYPE", "BAIDU_HANDWRITING_TYPE",
           "BAIDU_CUSTOM_TYPE",
           "BAIDU_GENERALBASIC_PAYLOAD", "BAIDU_GENERAL_PAYLOAD", "BAIDU_ACCURATE_PAYLOAD",
           "BAIDU_ACCURATEBASIC_PAYLOAD"]

logger = get_logger('Ocr')
baidu_ocr_urls = {}
baidu_ocr_payloads = {}
baidu_ocr_types = {}


def register_baidu_service(global_obj):
    def wrapper(func):
        dic = func()
        global_obj.update(dic)

    return wrapper


try:
    # Adaptive interface changes. It's recommended to do this via installed aip
    from aip import AipOcr

    for key, value in AipOcr.__dict__.items():
        if isinstance(value, str) and key.startswith('_AipOcr'):
            _ = key[9:].upper()[:-3]
            _key = 'BAIDU_' + _ + '_URL'
            baidu_ocr_urls[_key] = value

            if _key == 'BAIDU_GENERALBASIC_URL':
                BAIDU_GENERALBASIC_PAYLOAD = {}
                BAIDU_GENERALBASIC_PAYLOAD["language_type"] = "CHN_ENG"
                BAIDU_GENERALBASIC_PAYLOAD["detect_direction"] = "true"
                BAIDU_GENERALBASIC_PAYLOAD["detect_language"] = "true"
                BAIDU_GENERALBASIC_PAYLOAD["probability"] = "true"
                baidu_ocr_payloads['BAIDU_GENERALBASIC_PAYLOAD'] = BAIDU_GENERALBASIC_PAYLOAD
            if _key == 'BAIDU_GENERAL_URL':
                BAIDU_GENERAL_PAYLOAD = {}
                BAIDU_GENERAL_PAYLOAD["language_type"] = "CHN_ENG"
                BAIDU_GENERAL_PAYLOAD["detect_direction"] = "true"
                BAIDU_GENERAL_PAYLOAD["detect_language"] = "true"
                BAIDU_GENERAL_PAYLOAD["probability"] = "true"
                baidu_ocr_payloads['BAIDU_GENERAL_PAYLOAD'] = BAIDU_GENERAL_PAYLOAD

    for key in baidu_ocr_urls.keys():
        value = key[:-3] + 'TYPE'
        baidu_ocr_types[value] = value

except:
    logger.info('Recommended  to pip install aip')


    # Fixed api implementation, not recommended
    @register_baidu_service(global_obj=baidu_ocr_urls)
    def default_urls():
        res = {"BAIDU_GENERALBASIC_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic",
               "BAIDU_ACCURATEBASIC_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic",
               "BAIDU_GENERAL_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/general",
               "BAIDU_ACCURATE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate",
               "BAIDU_GENERALENHANCED_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/general_enhanced",
               "BAIDU_WEBIMAGE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage",
               "BAIDU_IDCARD_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard",
               "BAIDU_BANKCARD_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard",
               "BAIDU_DRIVINGLICENSE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/driving_license",
               "BAIDU_VEHICLELICENSE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/vehicle_license",
               "BAIDU_LICENSEPLATE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate",
               "BAIDU_BUSINESSLICENSE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license",
               "BAIDU_RECEIPT_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/receipt",
               "BAIDU_TRAINTICKET_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/train_ticket",
               "BAIDU_TAXIRECEIPT_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/taxi_receipt",
               "BAIDU_FORM_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/form",
               "BAIDU_TABLERECOGNIZE_URL": "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request",
               "BAIDU_TABLERESULTGET_URL": "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result",
               "BAIDU_VINCODE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/vin_code",
               "BAIDU_QUOTAINVOICE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/quota_invoice",
               "BAIDU_HOUSEHOLDREGISTER_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/household_register",
               "BAIDU_HKMACAUEXITENTRYPERMIT_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/HK_Macau_exitentrypermit",
               "BAIDU_TAIWANEXITENTRYPERMIT_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/taiwan_exitentrypermit",
               "BAIDU_BIRTHCERTIFICATE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/birth_certificate",
               "BAIDU_VEHICLEINVOICE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/vehicle_invoice",
               "BAIDU_VEHICLECERTIFICATE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/vehicle_certificate",
               "BAIDU_INVOICE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/invoice",
               "BAIDU_AIRTICKET_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/air_ticket",
               "BAIDU_INSURANCEDOCUMENTS_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/insurance_documents",
               "BAIDU_VATINVOICE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice",
               "BAIDU_QRCODE_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/qrcode",
               "BAIDU_NUMBERS_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers",
               "BAIDU_LOTTERY_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/lottery",
               "BAIDU_PASSPORT_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/passport",
               "BAIDU_BUSINESSCARD_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/business_card",
               "BAIDU_HANDWRITING_URL": "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting",
               "BAIDU_CUSTOM_URL": "https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise",
               }
        return res


    @register_baidu_service(global_obj=baidu_ocr_types)
    def default_types():
        res = {}
        for key in baidu_ocr_urls.keys():
            value = key[:-3] + 'TYPE'
            res[value] = value
        return res


finally:

    @register_baidu_service(global_obj=baidu_ocr_payloads)
    def default_payloads():
        BAIDU_GENERALBASIC_PAYLOAD = {}
        BAIDU_GENERALBASIC_PAYLOAD["language_type"] = "CHN_ENG"
        BAIDU_GENERALBASIC_PAYLOAD["detect_direction"] = "true"
        BAIDU_GENERALBASIC_PAYLOAD["detect_language"] = "true"
        BAIDU_GENERALBASIC_PAYLOAD["probability"] = "true"

        BAIDU_GENERAL_PAYLOAD = {}
        BAIDU_GENERAL_PAYLOAD["language_type"] = "CHN_ENG"
        BAIDU_GENERAL_PAYLOAD["detect_direction"] = "true"
        BAIDU_GENERAL_PAYLOAD["detect_language"] = "true"
        BAIDU_GENERAL_PAYLOAD["probability"] = "true"

        BAIDU_ACCURATE_PAYLOAD = {}
        BAIDU_ACCURATE_PAYLOAD["detect_direction"] = "true"

        BAIDU_ACCURATEBASIC_PAYLOAD = BAIDU_ACCURATE_PAYLOAD.copy()

        return {'BAIDU_GENERAL_PAYLOAD': BAIDU_GENERAL_PAYLOAD,
                'BAIDU_GENERALBASIC_PAYLOAD': BAIDU_GENERALBASIC_PAYLOAD,
                'BAIDU_ACCURATE_PAYLOAD': BAIDU_ACCURATE_PAYLOAD,
                'BAIDU_ACCURATEBASIC_PAYLOAD': BAIDU_ACCURATEBASIC_PAYLOAD}


    BAIDU_GENERALBASIC_TYPE = "BAIDU_GENERALBASIC_TYPE"
    BAIDU_ACCURATEBASIC_TYPE = "BAIDU_ACCURATEBASIC_TYPE"
    BAIDU_GENERAL_TYPE = "BAIDU_GENERAL_TYPE"
    BAIDU_ACCURATE_TYPE = "BAIDU_ACCURATE_TYPE"
    BAIDU_GENERALENHANCED_TYPE = "BAIDU_GENERALENHANCED_TYPE"
    BAIDU_WEBIMAGE_TYPE = "BAIDU_WEBIMAGE_TYPE"
    BAIDU_IDCARD_TYPE = "BAIDU_IDCARD_TYPE"
    BAIDU_BANKCARD_TYPE = "BAIDU_BANKCARD_TYPE"
    BAIDU_DRIVINGLICENSE_TYPE = "BAIDU_DRIVINGLICENSE_TYPE"
    BAIDU_VEHICLELICENSE_TYPE = "BAIDU_VEHICLELICENSE_TYPE"
    BAIDU_LICENSEPLATE_TYPE = "BAIDU_LICENSEPLATE_TYPE"
    BAIDU_BUSINESSLICENSE_TYPE = "BAIDU_BUSINESSLICENSE_TYPE"
    BAIDU_RECEIPT_TYPE = "BAIDU_RECEIPT_TYPE"
    BAIDU_TRAINTICKET_TYPE = "BAIDU_TRAINTICKET_TYPE"
    BAIDU_TAXIRECEIPT_TYPE = "BAIDU_TAXIRECEIPT_TYPE"
    BAIDU_FORM_TYPE = "BAIDU_FORM_TYPE"
    BAIDU_TABLERECOGNIZE_TYPE = "BAIDU_TABLERECOGNIZE_TYPE"
    BAIDU_TABLERESULTGET_TYPE = "BAIDU_TABLERESULTGET_TYPE"
    BAIDU_VINCODE_TYPE = "BAIDU_VINCODE_TYPE"
    BAIDU_QUOTAINVOICE_TYPE = "BAIDU_QUOTAINVOICE_TYPE"
    BAIDU_HOUSEHOLDREGISTER_TYPE = "BAIDU_HOUSEHOLDREGISTER_TYPE"
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
    BAIDU_LOTTERY_TYPE = "BAIDU_LOTTERY_TYPE"
    BAIDU_PASSPORT_TYPE = "BAIDU_PASSPORT_TYPE"
    BAIDU_BUSINESSCARD_TYPE = "BAIDU_BUSINESSCARD_TYPE"
    BAIDU_HANDWRITING_TYPE = "BAIDU_HANDWRITING_TYPE"
    BAIDU_CUSTOM_TYPE = "BAIDU_CUSTOM_TYPE"

    BAIDU_GENERALBASIC_PAYLOAD = baidu_ocr_payloads['BAIDU_GENERALBASIC_PAYLOAD']
    BAIDU_GENERAL_PAYLOAD = baidu_ocr_payloads['BAIDU_GENERAL_PAYLOAD']
    BAIDU_ACCURATE_PAYLOAD = baidu_ocr_payloads['BAIDU_ACCURATE_PAYLOAD']
    BAIDU_ACCURATEBASIC_PAYLOAD = baidu_ocr_payloads['BAIDU_ACCURATE_PAYLOAD']
