from enum import Enum
from typing import List, Optional, Union

class WhatsappMessageTemplateFormat(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    DOCUMENT = 'DOCUMENT'
    LOCATION = 'LOCATION'

class WhatsappMessageTemplateLanguage(Enum):
    es = 'es'
    es_AR = 'es_AR'
    es_ES = 'es_ES'
    es_MX = 'es_MX'

class WhatsappMessageTemplateCategory(Enum):
    AUTHENTICATION = 'AUTHENTICATION'
    MARKETING = 'MARKETING'
    UTILITY = 'UTILITY'

class WhatsappMessageComponentType(Enum):
    BODY = 'BODY'
    BUTTONS = 'BUTTONS'
    HEADER = 'HEADER'
    FOOTER = 'FOOTER'
    PHONE_NUMBER = 'PHONE_NUMBER'

class WMTEHeaderText:
    def __init__(self, header_text: str):
        self.header_text = header_text

class WMTEHeaderHandle:
    def __init__(self, header_handle: List[str]):
        self.header_handle = header_handle

class WMTEBodyText:
    def __init__(self, body_text: List[List[str]]):
        self.body_text = body_text

class WMTEButtonType(Enum):
    PHONE_NUMBER = 'PHONE_NUMBER'
    URL = 'URL'
    QUICK_REPLY = 'QUICK_REPLY'

class WMTEButton:
    def __init__(self, type: WMTEButtonType, text: str):
        self.type = type
        self.text = text

class WMTEButtonPhone(WMTEButton):
    def __init__(self, type: WMTEButtonType, text: str, phone_number: str):
        super().__init__(type, text)
        self.phone_number = phone_number

class WMTEButtonUrl(WMTEButton):
    def __init__(self, type: WMTEButtonType, text: str, url: str):
        super().__init__(type, text)
        self.url = url

class WhatsappMessageTemplateHeaderDto:
    def __init__(self, type: WhatsappMessageComponentType, header: str, format: WhatsappMessageTemplateFormat, text: str, example: Optional[Union[WMTEHeaderText, WMTEHeaderHandle]] = None):
        self.type = type
        self.header = header
        self.format = format
        self.text = text
        self.example = example

class Parameter:
    def __init__(self, type: str, text: str):
        self.type = type
        self.text = text

class WhatsappMessageTemplateBodyDto:
    def __init__(self, type: WhatsappMessageComponentType, parameters: List[Parameter], example: Optional[WMTEBodyText] = None):
        self.type = type
        self.parameters = parameters
        self.example = example

class WhatsappMessageTemplateButtonDto:
    def __init__(self, type: WhatsappMessageComponentType, buttons: List[Union[WMTEButtonPhone, WMTEButtonUrl, WMTEButton]]):
        self.type = type
        self.buttons = buttons

class WhatsappMessageTemplateFooterDto:
    def __init__(self, type: WhatsappMessageComponentType, text: str):
        self.type = type
        self.text = text

class WhatsappMessageComponentDto:
    pass

class Language:
    def __init__(self, code: str):
        self.code = code

class Template:
    def __init__(self, name: str, language: Language, components: Optional[List[Union[WhatsappMessageTemplateHeaderDto, WhatsappMessageTemplateBodyDto, WhatsappMessageTemplateButtonDto, WhatsappMessageTemplateFooterDto]]] = None):
        self.name = name
        self.language = language
        self.components = components

class MessageTemplateRequest:
    def __init__(self, messaging_product: str, recipient_type: str, to: str, type: str,template: Template):
        self.messaging_product = messaging_product
        self.recipient_type = recipient_type
        self.to = to
        self.type = type
        self.template = template

    def to_dict(self):
        return {
            "messaging_product": self.messaging_product,
            "recipient_type": self.recipient_type,
            "to": self.to,
            "type": self.type,
            "template": {
                "name": self.template.name,
                "language": { "code": self.template.language.code },
                "components": [
                    {
                        "type": component.type.value,
                        "parameters": [
                            { "type": param.type, "text": param.text } for param in component.parameters
                        ],
                    } for component in self.template.components
                ] if self.template.components else None
            }
        }
