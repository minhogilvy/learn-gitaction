import asyncio
import threading

from app.core.data_loader import get_data
from app.core.publisher import publisher
from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage, DocumentMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_text_message, send_interactive_message, send_document_message
from app.core.reports_states import ReportsStates
from app.utils.helpers import Helpers
from app.utils.state_utils import get_next_state
from app.constants import Constants


firebase_service = FirebaseService()
utils = Helpers()


async def handle_reports_start(user_id, data):
    reports_messages = data.reports_messages.messages
    reports_messages_please_wait = data.reports_messages_please_wait.messages
    session_id = firebase_service.get_latest_session_id_by_phone(user_id)
    data_firebase = firebase_service.get_user_data_by_sessions(user_id, session_id)
    if not data_firebase.get("gemini_data"):
        firebase_service.listen_document(user_id, session_id, reports_messages, handle_document_update)
        for message in reports_messages_please_wait:
            msg = WhatsAppMessage(to=user_id, body=message)
            await send_text_message(msg)
    else:
        parser_data = utils.parser_data_firebase(data_firebase)
        gemini_data = parser_data.gemini.parsed_data
        print("gemini_data" + str(gemini_data.get("calculus")))
        reports_messages[
            2] = f"Calculus: {gemini_data.get('calculus')}\n\n Gingivitis: {gemini_data.get('gingivitis')}\n\n Mouth Ulcers: {gemini_data.get('mouthUlcers')}\n\n Discoloration: {gemini_data.get('discoloration')}\n\n Caries: {gemini_data.get('caries')}"
        await send_messages(user_id, session_id, reports_messages, parser_data)


async def handle_reports_start_process(user_id, message, data, route_to_state_handler):
    user_input = message.text.body.lower()
    if user_input == Constants.REPORTS_INPUT_TYPE:
        next_state = get_next_state(ReportsStates.REPORT_START_PROCESS, "valid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(ReportsStates.REPORT_START_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    
    await route_to_state_handler(user_id, ReportsStates.REPORT_START_PROCESS, "invalid_response", next_state, message)


async def handle_report_valid(user_id, data):
    session_id = firebase_service.get_latest_session_id_by_phone(user_id)
    data_firebase = utils.get_user_data(user_id, session_id)
    
    if not data_firebase.report_url:
        reports_messages_please_wait = data.reports_messages_please_wait.messages
        firebase_service.listen_document(user_id, session_id, data, handle_document_reports_url)
        for message in reports_messages_please_wait:
            msg = WhatsAppMessage(to=user_id, body=message)
            await send_text_message(msg)
    else:
        await send_messages_with_url(user_id, session_id, data, data_firebase)


async def handle_report_valid_message(user_id, data):
    help_message = data.reports_generation_pdf.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=help_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(ReportsStates.REPORT_VALID, "default")
    firebase_service.save_user_state(user_id, next_state)


async def handle_report_invalid(user_id, data):
    for msg in data.reports_invalid_input_messages.messages:
        await send_text_message(WhatsAppMessage(to=user_id, body=msg))
    next_state = get_next_state(ReportsStates.REPORT_INVALID, "default")
    firebase_service.save_user_state(user_id, next_state)


async def handle_report_invalid_again(user_id, data):
    for msg in data.reports_invalid_input_messages_again.messages:
        await send_text_message(WhatsAppMessage(to=user_id, body=msg))
    
    await handle_report_invalid(user_id, data)
    next_state = get_next_state(ReportsStates.REPORT_INVALID_AGAIN, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_report_invalid_process(user_id, message, data, route_to_state_handler):
    user_input = message.text.body.lower()
    if user_input == Constants.REPORTS_INPUT_TYPE:
        next_state = get_next_state(ReportsStates.REPORT_INVALID_PROCESS, "valid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(ReportsStates.REPORT_INVALID_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    
    await route_to_state_handler(user_id, ReportsStates.REPORT_INVALID_PROCESS, "default", next_state, message)


async def send_messages(user_id, session_id, messages, parser_data):
    if firebase_service.is_listening(user_id, session_id):
        # Use a separate thread to unsubscribe to avoid joining the current thread
        threading.Thread(target=firebase_service.unsubscribe, args=(user_id, session_id)).start()
    
    if not parser_data.report_url:
        utils.generate_report(user_id, session_id)
    for message in messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    
    next_state = get_next_state(ReportsStates.REPORT_START, "default")
    firebase_service.save_user_state(user_id, next_state)


async def send_messages_with_url(user_id, session_id, data_messages, data_firebase):
    if firebase_service.is_listening(user_id, session_id):
        # Use a separate thread to unsubscribe to avoid joining the current thread
        threading.Thread(target=firebase_service.unsubscribe, args=(user_id, session_id)).start()
    
    msg_pdf_url = data_messages.reports_pdf_url.messages[0]
    await send_text_message(WhatsAppMessage(to=user_id, body=msg_pdf_url))
    pdf_url = data_firebase.report_url
    await send_document_message(DocumentMessage(to=user_id, link=pdf_url, filename="Oral_basic_report"))
    await asyncio.sleep(1)
    for msg in data_messages.reports_generation_pdf.messages:
        await send_text_message(WhatsAppMessage(to=user_id, body=msg))
    help_message = data_messages.reports_generation_pdf.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=help_message.dict())
    await send_interactive_message(interactive_msg)
    
    next_state = get_next_state(ReportsStates.REPORT_VALID, "default")
    firebase_service.save_user_state(user_id, next_state)


def handle_document_reports_url(user_id, session_id, data_messages, data):
    data_firebase = utils.parser_data_firebase(data)
    if data_firebase.report_url:
        asyncio.run(send_messages_with_url(user_id, session_id, data_messages, data_firebase))


def handle_document_update(user_id, session_id, reports_messages, data):
    # Update reports_messages with the new data and send messages
    parser_data = utils.parser_data_firebase(data)
    gemini_data = parser_data.gemini.parsed_data
    reports_messages[
        2] = f"Calculus: {gemini_data.get('calculus')}\n\n Gingivitis: {gemini_data.get('gingivitis')}\n\n Mouth Ulcers: {gemini_data.get('mouthUlcers')}\n\n Discoloration: {gemini_data.get('discoloration')}\n\n Caries: {gemini_data.get('caries')}"
    asyncio.run(send_messages(user_id, session_id, reports_messages, parser_data))
