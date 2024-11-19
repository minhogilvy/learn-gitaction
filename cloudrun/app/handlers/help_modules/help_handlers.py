from app.core.data_loader import get_data
from app.core.dental_analysis_states import DentalAnalysisStates
from app.core.reports_states import ReportsStates
from app.core.welcome_states import WelcomeStates
from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_interactive_message, send_text_message
from app.core.help_states import HelpStates
from app.utils.state_utils import get_next_state


firebase_service = FirebaseService()


async def handle_help_start(user_id, data):
    interactive_message = data.help_start.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=interactive_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(HelpStates.HELP_START, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_help_start_response(user_id, message, data, route_to_state_handler):
    user_response_id = message.interactive.button_reply.id
    next_state = get_next_state(HelpStates.HELP_START_PROCESS, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, HelpStates.HELP_START_PROCESS, user_response_id, next_state, message)


async def handle_help_make_new_assessment(user_id, data):
    new_assessment_message = data.help_make_new_assessment.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=new_assessment_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(HelpStates.HELP_MAKE_NEW_ASSESSMENT, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_help_make_new_assessment_response(user_id, message, data, route_to_state_handler):
    user_response_id = message.interactive.button_reply.id
    
    next_state = get_next_state(HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS, user_response_id, next_state, message)


async def handle_help_more_about_oral_care(user_id, data):
    for msg in data.help_more_about_oral_care.messages:
        await send_text_message(WhatsAppMessage(to=user_id, body=msg))
    
    oral_care_message = data.help_more_about_oral_care.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=oral_care_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(HelpStates.HELP_MORE_ABOUT_ORAL_CARE, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_help_more_about_oral_care_response(user_id, message, data, route_to_state_handler):
    user_response_id = message.interactive.button_reply.id
    
    next_state = get_next_state(HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS, user_response_id, next_state, message)


async def handle_help_create_report_again(user_id, data):
    oral_care_message = data.help_create_report_again.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=oral_care_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(HelpStates.HELP_CREATE_REPORT_AGAIN, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_help_create_report_again_process_response(user_id, message, data, route_to_state_handler):
    user_response_id = message.interactive.button_reply.id
    
    next_state = get_next_state(HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS, user_response_id)
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS, user_response_id, next_state, message)


async def handle_help_keep_my_data(user_id, data, route_to_state_handler):
    for msg in data.help_keep_my_data.messages:
        await send_text_message(WhatsAppMessage(to=user_id, body=msg))
    await handle_help_start(user_id, data)
    next_state = get_next_state(HelpStates.HELP_START, "default")
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, HelpStates.HELP_START, "default", next_state, data)


async def handle_help_nothing_thats_all(user_id, data, route_to_state_handler):
    next_state = get_next_state(HelpStates.HELP_NOTHING_THATS_ALL, "default")
    firebase_service.save_user_state(user_id, next_state)
    # Transition to the feedback rating state
    await route_to_state_handler(user_id, HelpStates.HELP_NOTHING_THATS_ALL, "default", "feedback_rating_start", data)


async def handle_help_yes_do_it(user_id, data, data_dental_analysis):
    ready_prompt_message = data_dental_analysis.ready_prompt_dental_analysis.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=ready_prompt_message.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.reset_user_score(user_id)
    firebase_service.save_user_state(user_id, DentalAnalysisStates.START)


async def handle_help_no(user_id, data):
    help_message = data.reports_generation_pdf.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=help_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(ReportsStates.REPORT_VALID_MESSAGE, "default")
    firebase_service.save_user_state(user_id, next_state)


async def handle_help_for_someone_else(user_id, data, route_to_state_handler):
    next_state = get_next_state(WelcomeStates.WELCOME_PRIVACY_POLICY, "default")
    firebase_service.create_user(user_id)
    # Transition to the feedback rating state
    await route_to_state_handler(user_id, WelcomeStates.WELCOME_PRIVACY_POLICY, "default", next_state, data)