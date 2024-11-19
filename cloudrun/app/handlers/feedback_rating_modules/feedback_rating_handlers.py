from app.core.feedback_rating_states import FeedbackRatingStates
from app.core.help_states import HelpStates
from app.core.reports_states import ReportsStates
from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage
from app.constants import Constants
from app.services.firebase import FirebaseService
from app.services.message_service import send_interactive_message, send_text_message
from app.utils.helpers import Helpers
from app.utils.state_utils import get_next_state


firebase_service = FirebaseService()

utils = Helpers()


async def handle_feedback_rating_start(user_id, data):
    feedback_start_message = data.feedback_rating_start.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=feedback_start_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_START, "default")
    firebase_service.save_user_state(user_id, next_state)


async def handle_feedback_rating_start_process(user_id, message, data, route_to_state_handler):
    user_input = message.interactive.button_reply.id
    next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS, user_input)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS, user_input, next_state, message)


async def handle_feedback_rating_yes_sure(user_id, data):
    feedback_yes_sure_message = data.feedback_rating_yes_sure.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=feedback_yes_sure_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_YES_SURE, "default")
    firebase_service.save_user_state(user_id, next_state)


async def handle_feedback_rating_yes_sure_process(user_id, message, data, route_to_state_handler):
    user_input = message.interactive.list_reply.id
    user_select = message.interactive.list_reply.title
    if user_input in ['fair', 'good', 'excellent']:
        next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS, "feedback_rating_excellent")
        firebase_service.save_user_data(user_id, {"feedback_rating": user_select})
    else:
        next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS, "feedback_rating_poor")
        firebase_service.save_user_data(user_id, {"feedback_rating": user_select})
    
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS, user_input, next_state, message)


async def handle_feedback_rating_no_thanks(user_id, data):
    feedback_no_thanks_message = data.feedback_rating_no_thanks.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=feedback_no_thanks_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS, "default")
    firebase_service.save_user_state(user_id, next_state)


async def handle_feedback_rating_no_thanks_process(user_id, message, data, route_to_state_handler):
    user_input = message.interactive.button_reply.id
    next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS_PROCESS, user_input)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS_PROCESS, user_input, next_state, message)


async def handle_feedback_rating_excellent(user_id, data):
    feedback_excellent_message = data.feedback_rating_excellent.messages
    for message in feedback_excellent_message:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    
    await handle_feedback_rating_no_thanks(user_id, data)


async def handle_feedback_rating_poor(user_id, data):
    feedback_poor_message = data.feedback_rating_poor.messages
    for message in feedback_poor_message:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_POOR, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_feedback_rating_poor_process(user_id, message, data, route_to_state_handler):
    user_input = message.text.body
    if utils.count_total_characters(user_input) <= 255:
        next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_POOR_PROCESS, "valid_response")
        firebase_service.save_user_data(user_id, {"feedback_comments": user_input})
    else:
        next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_POOR_PROCESS, "invalid_response")
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, FeedbackRatingStates.FEEDBACK_RATING_POOR_PROCESS, "default", next_state, message)


async def handle_feedback_rating_poor_invalid(user_id, data):
    feedback_poor_invalid_message = data.feedback_rating_poor_invalid.messages
    for message in feedback_poor_invalid_message:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_feedback_rating_poor_invalid_process(user_id, message, data, route_to_state_handler):
    user_input = message.text.body
    if utils.count_total_characters(user_input) <= 255:
        next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID_PROCESS, "valid_response")
        firebase_service.save_user_data(user_id, {"feedback_comments": user_input})
    else:
        next_state = get_next_state(FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID_PROCESS, "invalid_response")
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID_PROCESS, "default", next_state, message)


async def handle_feedback_rating_start_conversation(user_id, message, data, route_to_state_handler):
    interactive_message = data.help_start.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=interactive_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(HelpStates.HELP_START, "default")
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, HelpStates.HELP_START, "default", next_state, data)


async def handle_feedback_rating_poor_valid(user_id, message, data, route_to_state_handler):
    message_valid = data.feedback_rating_poor_valid.messages[0]
    msg = WhatsAppMessage(to=user_id, body=message_valid)
    await send_text_message(msg)
    await handle_feedback_rating_start_conversation(user_id, message, data, route_to_state_handler)
