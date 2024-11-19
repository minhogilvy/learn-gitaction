from app.model.bot_opt_in_data import BotOptInData
from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_interactive_message, send_text_message
from app.constants import Constants
from app.core.welcome_states import WelcomeStates
from app.core.data_loader import get_data
from app.utils.helpers import Helpers
from app.utils.state_utils import get_next_state
from app.utils.validators import check_valid, check_valid_interactive


firebase_service = FirebaseService()
utils = Helpers()


async def handle_accept_state(user_id):
    data = get_data()
    thank_you_messages = data.thank_you
    
    for message in thank_you_messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    
    # Save user state
    firebase_service.save_user_state(user_id, WelcomeStates.THANK_YOU)


async def handle_i_agree_state(user_id):
    data = get_data()
    thank_you_messages = data.thank_you
    
    for message in thank_you_messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    
    # Save user state
    firebase_service.save_user_state(user_id, WelcomeStates.THANK_YOU)


async def handle_i_disagree_state(user_id):
    data = get_data()
    i_disagree_message = data.i_disagree.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=i_disagree_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(WelcomeStates.I_DISAGREE, "default")
    # Save user state
    firebase_service.save_user_state(user_id, next_state)


async def handle_i_disagree_process_state(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    i_disagree = data.i_disagree.interactive
    if not check_valid_interactive(user_response_id, i_disagree):
        await handle_i_disagree_state(user_id)
    else:
        if user_response_id == "i_stop_here":
            next_state = get_next_state(WelcomeStates.I_DISAGREE_PROCESS, "i_stop_here")
        else:
            next_state = get_next_state(WelcomeStates.I_DISAGREE_PROCESS, "i_accept")
        
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, WelcomeStates.I_DISAGREE_PROCESS, user_response_id, next_state, message)


async def handle_restart_state(user_id):
    data = get_data()
    restart_messages = data.welcome_privacy_policy.messages
    
    for message in restart_messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    
    # Resend interactive message
    interactive_message = data.welcome_privacy_policy.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=interactive_message.dict())
    await send_interactive_message(interactive_msg)
    
    # Save user state
    firebase_service.save_user_state(user_id, WelcomeStates.WELCOME_PRIVACY_POLICY)


async def handle_stop_state(user_id):
    data = get_data()
    stop_message = data.stop.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=stop_message.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(WelcomeStates.STOP, "default")
    
    # Save user state
    firebase_service.save_user_state(user_id, next_state)


async def handle_stop_process_state(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    stop = data.stop.interactive
    if not check_valid_interactive(user_response_id, stop):
        await handle_stop_state(user_id)
    else:
        next_state = get_next_state(WelcomeStates.STOP_PROCESS, user_response_id)
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, WelcomeStates.STOP_PROCESS, user_response_id, next_state, message)


async def handle_show_terms_policy_state(user_id):
    data = get_data()
    terms_policy_message = data.show_policy_privacy.messages[0]
    terms_policy_interactive = data.show_policy_privacy.interactive
    message_msg = WhatsAppMessage(to=user_id, body=terms_policy_message)
    interactive_msg = InteractiveMessage(to=user_id, interactive=terms_policy_interactive.dict())
    await send_text_message(message_msg)
    await send_interactive_message(interactive_msg)
    
    # Save user state
    firebase_service.save_user_state(user_id, WelcomeStates.SHOW_TERMS_POLICY_PROCESS)


async def process_show_terms_policy_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    terms_policy_interactive = data.show_policy_privacy.interactive
    if not check_valid_interactive(user_response_id, terms_policy_interactive):
        await handle_show_terms_policy_state(user_id)
    else:
        if user_response_id == "show_policy_privacy_i_agree":
            next_state = get_next_state(WelcomeStates.SHOW_TERMS_POLICY_PROCESS, "show_policy_privacy_i_agree")
        else:
            next_state = get_next_state(WelcomeStates.SHOW_TERMS_POLICY_PROCESS, "show_policy_privacy_i_disagree")
        
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, WelcomeStates.SHOW_TERMS_POLICY_PROCESS, user_response_id, next_state, message)


async def handle_thank_you_state(user_id, messages, data, route_to_state_handler):
    
    for message in messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    
    next_state = get_next_state(WelcomeStates.THANK_YOU, "default")
    firebase_service.save_user_state(user_id, next_state)
    bot_data = BotOptInData(
        bot_opt_in=True,
        promo_opt_in=True,
        privacy_agreement=True,
        opt_in_date=utils.get_date()
    )
    utils.set_consent_action(user_id, Constants.ACTION_TYPE_CONSENT)
    firebase_service.save_user_data(user_id, bot_data.dict(by_alias=True))
    await route_to_state_handler(user_id, WelcomeStates.THANK_YOU, "default", next_state, data)


async def handle_welcome_privacy_policy_state(user_id):
    data = get_data()
    messages = data.welcome_privacy_policy.messages
    interactive_message = data.welcome_privacy_policy.interactive
    
    for message in messages:
        msg = WhatsAppMessage(to=user_id, body=message)
        await send_text_message(msg)
    
    interactive_msg = InteractiveMessage(to=user_id, interactive=interactive_message.dict())
    await send_interactive_message(interactive_msg)
    
    # Save user state
    firebase_service.save_user_state(user_id, WelcomeStates.WELCOME_PRIVACY_POLICY)
