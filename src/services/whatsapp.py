import requests
from src.core.config import settings
from src.models.whatsapp import MessageTemplateRequest, Template, \
    WhatsappMessageTemplateBodyDto, Parameter, WhatsappMessageComponentType, \
    Language
from src.models.user import User
from src.models.fund import Fund

WHATSAPP_URL=settings.WHATSAPP_URL

class WhatsappService:
    @staticmethod
    def send_message(user: User, fund: Fund):
        try:
            headers = {
                "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }

            template_component = WhatsappMessageTemplateBodyDto(
                type=WhatsappMessageComponentType.BODY,
                parameters=[
                    Parameter(type="text", text=user["name"]),
                    Parameter(type="text", text=fund["name"]),
                    Parameter(type="text", text=fund['minimum_amount'])
                ]
            )

            template = Template(
                name=settings.WHATSAPP_TEMPLATE_NAME,
                language=Language(code="en"),
                components=[template_component]
            )

            data = MessageTemplateRequest(
                messaging_product="whatsapp",
                recipient_type="individual",
                to=settings.FIRED_WHATSAPP_NUMBER,
                type="template",
                template=template
            )

            data_dict = data.to_dict()

            response = requests.post(f"{WHATSAPP_URL}/{settings.WHATSAPP_NUMBER_ID}/messages", headers=headers, json=data_dict)
            response.raise_for_status()

            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            print(f"[ERROR] WhatsappService.HTTP error occurred: {http_err}")
            print(f"[ERROR] WhatsappService.Response content: {http_err.response.content}")
        except Exception as e:
            print(f"[ERROR] WhatsappService.send_message: {str(e)}")
            raise e
