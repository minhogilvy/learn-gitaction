import asyncio

from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage, VideoMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_interactive_message, send_text_message, send_video_message
from app.core.tutorial_states import TutorialStates
from app.utils.state_utils import get_next_state
from app.constants import Constants


firebase_service = FirebaseService()


async def handle_start_tutorial(user_id, data):
    tutorial_message = data.tutorial.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=tutorial_message.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, TutorialStates.START_TUTORIAL)


async def handle_watch_tutorial_prompt(user_id, data):
    watch_tutorial_prompt_message = data.tutorial_check.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=watch_tutorial_prompt_message.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, TutorialStates.VIEW_TUTORIAL_CHECK)


async def handle_view_tutorial_check(user_id, data):
    tutorial_check_message = data.tutorial_check.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=tutorial_check_message.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, TutorialStates.VIEW_TUTORIAL_CHECK)


async def process_view_tutorial_check_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    
    if user_response_id == 'yes_all_good':
        next_state = get_next_state(TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS, "yes_all_good")
    else:
        message_video = data.tutorial_check_message.messages[0]
        await send_text_message(WhatsAppMessage(to=user_id, body=message_video))
        next_state = get_next_state(TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS, "no_i_wasnt_able_to")
    
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS, user_response_id, next_state, message)


async def handle_view_tutorial_yes_all_good_check(user_id, data):
    message = data.tutorial_video_text.messages[0]
    link = firebase_service.generate_signed_url(Constants.TUTORIAL_VIDEO_URL)
    await send_text_message(WhatsAppMessage(to=user_id, body=message))
    await send_video_message(VideoMessage(to=user_id, link=link))
    await asyncio.sleep(0.5)
    proceed_prompt_message = data.proceed_prompt.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=proceed_prompt_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_view_tutorial_yes_all_good_process_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    
    next_state = get_next_state(TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS, user_response_id, next_state, message)


async def process_proceed_prompt_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    
    if user_response_id == 'sure':
        next_state = get_next_state(TutorialStates.PROCEED_PROMPT, "sure")
    else:
        ready_prompt_message = data.ready_prompt.interactive
        interactive_msg = InteractiveMessage(to=user_id, interactive=ready_prompt_message.dict())
        await send_interactive_message(interactive_msg)
        next_state = get_next_state(TutorialStates.PROCEED_PROMPT, "not_yet")
    
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, TutorialStates.PROCEED_PROMPT, user_response_id, next_state, message)


async def process_ready_prompt_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    
    next_state = get_next_state(TutorialStates.READY_PROMPT, "im_ready")
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, TutorialStates.READY_PROMPT, user_response_id, next_state, message)
