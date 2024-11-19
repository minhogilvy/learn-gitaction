import httpx
import asyncio
from app.constants import Constants
from app.schemas.whatsapp.message import WhatsAppMessage, InteractiveMessage, ImageMessage, VideoMessage, DocumentMessage
from app.services.firebase import FirebaseService
from app.utils.helpers import Helpers


firebase_service = FirebaseService()
utils = Helpers()


async def send_request_with_retry(url, headers, data, retries=2):
    delay = 0.3
    for attempt in range(retries):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return True
            else:
                response_json = response.json()
                print(response_json)
                if response.status_code == 429 or (
                        'error' in response_json and response_json['error'].get('code') == 131056
                ):
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
                        delay *= 2  # Exponential backoff
                    else:
                        return False
                else:
                    return False
    return False


async def send_text_message(message: WhatsAppMessage):
    url = f"{Constants.MESSAGES_WHATSAPP_API_URL}"
    phone_number = message.to
    message.to = utils.decrypt(message.to)
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "text",
        "text": {
            "body": message.body
        }
    }
    firebase_service.save_user_history(phone_number, message.body, Constants.HISTORY_BOT)
    return await send_request_with_retry(url, headers, data)


async def send_document_message(message: DocumentMessage):
    url = f"{Constants.MESSAGES_WHATSAPP_API_URL}"
    phone_number = message.to
    message.to = utils.decrypt(message.to)
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": message.to,
        "type": "document",
        "document": {
            "link": message.link,
            "caption": message.caption,
            "filename": message.filename
        }
    }
    firebase_service.save_user_history(phone_number, f"document : {message.link}", Constants.HISTORY_BOT)
    return await send_request_with_retry(url, headers, data)


async def send_interactive_message(message: InteractiveMessage):
    url = f"{Constants.MESSAGES_WHATSAPP_API_URL}"
    phone_number = message.to
    message.to = utils.decrypt(message.to)
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "interactive",
        "interactive": message.interactive
    }
    firebase_service.save_user_history(phone_number, message.interactive.get('body').get("text"), Constants.HISTORY_BOT)
    return await send_request_with_retry(url, headers, data)


async def send_image_message(message: ImageMessage):
    url = f"{Constants.MESSAGES_WHATSAPP_API_URL}"
    phone_number = message.to
    message.to = utils.decrypt(message.to)
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "image",
        "image": {
            "link": message.link,
            "caption": message.caption
        }
    }
    firebase_service.save_user_history(phone_number, f"Image : {message.link}", Constants.HISTORY_BOT)
    return await send_request_with_retry(url, headers, data)


async def send_video_message(message: VideoMessage):
    url = f"{Constants.MESSAGES_WHATSAPP_API_URL}"
    phone_number = message.to
    message.to = utils.decrypt(message.to)
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "video",
        "video": {
            "link": message.link,
            "caption": message.caption
        }
    }
    firebase_service.save_user_history(phone_number, f"Video : {message.link}", Constants.HISTORY_BOT)
    return await send_request_with_retry(url, headers, data)
