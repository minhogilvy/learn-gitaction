import asyncio

from app.config import get_settings
from app.core.data_loader import parse_res_image
from app.core.publisher import publisher
from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage, ImageMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_interactive_message, send_text_message, send_image_message
from app.core.dental_analysis_states import DentalAnalysisStates
from app.services.tensorflow_ai import TensorflowAI
from app.utils.helpers import Helpers
from app.utils.state_utils import get_next_state
from app.constants import Constants


firebase_service = FirebaseService()
model = TensorflowAI()
utils = Helpers()


async def handle_dental_analysis(user_id, data):
    tips_message = data.dental_analysis.messages[0]
    await send_text_message(WhatsAppMessage(to=user_id, body=tips_message))
    next_message = data.ready_prompt_dental_analysis.messages[0]
    await send_text_message(WhatsAppMessage(to=user_id, body=next_message))
    ready_prompt_message = data.ready_prompt_dental_analysis.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=ready_prompt_message.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, DentalAnalysisStates.START)


async def process_ready_prompt_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    
    next_state = get_next_state(DentalAnalysisStates.START, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, DentalAnalysisStates.START, user_response_id, next_state, message)


async def handle_lower_teeth_prompt(user_id, message, data, route_to_state_handler):
    
    for message in data.lower_teeth.messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    link = firebase_service.generate_signed_url(Constants.LOWER_TEETH_IMAGE_MIRROR_URL)
    await send_image_message(ImageMessage(to=user_id, link=link))
    await asyncio.sleep(0.5)
    message_photo = data.lower_teeth_the_photo.messages[0]
    msg_photo = WhatsAppMessage(to=user_id, body=message_photo)
    await send_text_message(msg_photo)
    link = firebase_service.generate_signed_url(Constants.LOWER_TEETH_IMAGE_URL)
    await send_image_message(ImageMessage(to=user_id, link=link))
    
    next_state = get_next_state(DentalAnalysisStates.LOWER_TEETH_PROMPT, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_lower_teeth_response(user_id, message, data, route_to_state_handler, background_tasks):
    if check_valid_lower_teeth(message.image):
        upload_image_background(user_id, message, Constants.BUCKET_NAME_LOWER_JAW_IMAGE)
        next_state = get_next_state(DentalAnalysisStates.LOWER_TEETH_PROMPT_PROCESS, "valid_response")
        
        # Move to the next state if the image is valid
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, DentalAnalysisStates.LOWER_TEETH_PROMPT_PROCESS, "valid_response", next_state, message)
    else:
        invalid_message = data.invalid_messages.invalid_lower_teeth_message
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = get_next_state(DentalAnalysisStates.LOWER_TEETH_PROMPT_PROCESS, "invalid_response")
        
        # Update state to invalid response
        firebase_service.save_user_state(user_id, next_state)


async def handle_upper_teeth_prompt(user_id, message, data, route_to_state_handler):
    for message in data.upper_teeth.messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    link = firebase_service.generate_signed_url(Constants.UPPER_TEETH_IMAGE_MIRROR_URL)

    await send_image_message(ImageMessage(to=user_id, link=link))
    await asyncio.sleep(0.5)
    message_photo = data.lower_teeth_the_photo.messages[0]
    msg_photo = WhatsAppMessage(to=user_id, body=message_photo)
    await send_text_message(msg_photo)
    link = firebase_service.generate_signed_url(Constants.UPPER_TEETH_IMAGE_URL)
    await send_image_message(ImageMessage(to=user_id, link=link))
    
    next_state = get_next_state(DentalAnalysisStates.UPPER_TEETH_PROMPT, "default")
    firebase_service.save_user_state(user_id, next_state)


async def handle_ready_prompt(user_id, message, data, route_to_state_handler):
    ready_prompt_message = data.ready_prompt_process_dental_analysis.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=ready_prompt_message.dict())
    await send_interactive_message(interactive_msg)
    
    next_state = get_next_state(DentalAnalysisStates.READY_PROMPT, "default")
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, DentalAnalysisStates.READY_PROMPT, "default", next_state, message)


async def process_upper_teeth_response(user_id, message, data, route_to_state_handler, background_tasks):
    if check_valid_upper_teeth(message.image):
        upload_image_background(user_id, message, Constants.BUCKET_NAME_UPPER_JAW_IMAGE)
        next_state = get_next_state(DentalAnalysisStates.UPPER_TEETH_PROMPT_PROCESS, "valid_response")
        
        # Move to the next state if the image is valid
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, DentalAnalysisStates.UPPER_TEETH_PROMPT_PROCESS, "valid_response", next_state, message)
    else:
        invalid_message = data.invalid_messages.invalid_upper_teeth_message
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = get_next_state(DentalAnalysisStates.UPPER_TEETH_PROMPT_PROCESS, "invalid_response")
        
        # Update state to invalid response
        firebase_service.save_user_state(user_id, next_state)


async def handle_front_teeth_prompt(user_id, message, data, route_to_state_handler):
    for message in data.front_teeth.messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    link = firebase_service.generate_signed_url(Constants.FRONT_TEETH_IMAGE_MIRROR_URL)
    await send_image_message(ImageMessage(to=user_id, link=link))
    await asyncio.sleep(0.5)
    message_photo = data.lower_teeth_the_photo.messages[0]
    msg_photo = WhatsAppMessage(to=user_id, body=message_photo)
    await send_text_message(msg_photo)
    link = firebase_service.generate_signed_url(Constants.FRONT_TEETH_IMAGE_URL)
    await send_image_message(ImageMessage(to=user_id, link=link))
    
    next_state = get_next_state(DentalAnalysisStates.FRONT_TEETH_PROMPT, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_front_teeth_response(user_id, message, data, route_to_state_handler, background_tasks):
    if check_valid_front_teeth(message.image):
        upload_image_background(user_id, message, Constants.BUCKET_NAME_FRONT_TEETH_IMAGE)

        next_state = get_next_state(DentalAnalysisStates.FRONT_TEETH_PROMPT_PROCESS, "valid_response")
        
        # Move to the next state if the image is valid
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, DentalAnalysisStates.FRONT_TEETH_PROMPT_PROCESS, "valid_response", next_state, message)
    else:
        invalid_message = data.invalid_messages.invalid_front_teeth_message
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = get_next_state(DentalAnalysisStates.FRONT_TEETH_PROMPT_PROCESS, "invalid_response")
        
        # Update state to invalid response
        firebase_service.save_user_state(user_id, next_state)


async def handle_thank_you_analyze(user_id, data):
    # Send the initial thank you message
    thank_you_message = data.thank_you_analyze.messages[0]
    await send_text_message(WhatsAppMessage(to=user_id, body=thank_you_message))
    
    # Send the interactive message asking for consent to ask questions
    analyze_question_message = data.thank_you_analyze.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=analyze_question_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(DentalAnalysisStates.THANK_YOU_ANALYZE, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_thank_you_analyze_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    
    next_state = get_next_state(DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS, user_response_id, next_state, message)


async def handle_thank_you_analyze_not_now_response(user_id, message, data):
    # Send the follow-up interactive button
    follow_up_interactive = data.thank_you_analyze_reminder_button.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=follow_up_interactive.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_thank_you_analyze_not_now_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    
    next_state = get_next_state(DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW_PROCESS, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW_PROCESS, user_response_id, next_state, message)


def upload_image_background(user_id, message, file_name):
    session_id = firebase_service.get_latest_session_id_by_phone(user_id)
    payload = {
        'queue_type': Constants.QUEUE_UPLOAD_IMAGE,
        'document_id': user_id,
        'session_id': session_id,
        'image_id': message.image.id,
        'file_name': file_name
    }
    response = publisher(payload)
    print("response: " + str(response))
    # image_url = upload_image(user_id, image=message.image, file_name=file_name)
    # firebase_service.save_user_data(user_id, {file_name: image_url})



def check_valid_lower_teeth(image):
    predictions = check_predict_image(image)
    return predictions['className'].replace("\n", "") == Constants.KEY_LOWER_JAW


def check_valid_upper_teeth(image):
    predictions = check_predict_image(image)
    return predictions['className'].replace("\n", "") == Constants.KEY_UPPER_JAW


def check_valid_front_teeth(image):
    predictions = check_predict_image(image)
    return predictions['className'].replace("\n", "") == Constants.KEY_FRONT_TEETH


def check_predict_image(image):
    res_image = utils.get_retrieve_media_url(image.id)
    parsed_image = parse_res_image(res_image)
    sorted_predictions = model.predict_image(parsed_image.url)
    print("sorted_predictions: " + str(sorted_predictions))
    return sorted_predictions[0]


