from app.core.data_country import get_countries
from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_interactive_message, send_text_message
from app.core.personal_information_states import PersonalInformationStates
from app.utils.helpers import Helpers
from app.utils.state_utils import get_next_state
from app.utils.validators import is_valid_name, is_valid_email, is_valid_country, is_valid_phone_number, is_valid_date_of_birth, is_age_valid_and_18_or_older, is_age_valid_range, check_valid, \
    check_valid_interactive


firebase_service = FirebaseService()
utils = Helpers()


async def handle_gender_state(user_id, data):
    gender_message = data.gender.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=gender_message.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.SELECT_GENDER)


async def process_gender_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.list_reply.id
    else:
        user_response_id = "default"
    
    if user_response_id in ['male', 'female', 'prefer_not_to_say', 'other']:
        next_state = get_next_state(PersonalInformationStates.SELECT_GENDER_PROCESS, "valid_response")
        firebase_service.save_user_data(user_id, {"gender": message.interactive.list_reply.title})
    else:
        next_state = get_next_state(PersonalInformationStates.SELECT_GENDER_PROCESS, "invalid_response")
    
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, PersonalInformationStates.SELECT_GENDER_PROCESS, user_response_id, next_state, message)


async def handle_first_name_state(user_id, data):
    first_name_message = data.first_name.messages[0]
    msg = WhatsAppMessage(to=user_id, body=first_name_message)
    await send_text_message(msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.FIRST_NAME)


async def process_first_name_response(user_id, message, data, route_to_state_handler):
    user_first_name = message.text.body
    
    if is_valid_name(user_first_name):
        firebase_service.save_user_data(user_id, {"first_name": user_first_name})
        next_state = get_next_state(PersonalInformationStates.FIRST_NAME_PROCESS, "default")
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, PersonalInformationStates.FIRST_NAME_PROCESS, "default", next_state, message)
    else:
        invalid_message = data.invalid_messages.invalid_full_name
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = PersonalInformationStates.FIRST_NAME
        firebase_service.save_user_state(user_id, next_state)


async def handle_last_name_state(user_id, data):
    last_name_message = data.last_name.messages[0]
    msg = WhatsAppMessage(to=user_id, body=last_name_message)
    await send_text_message(msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.LAST_NAME)


async def process_last_name_response(user_id, message, data, route_to_state_handler):
    user_last_name = message.text.body
    
    if is_valid_name(user_last_name):
        firebase_service.save_user_data(user_id, {"last_name": user_last_name})
        next_state = get_next_state(PersonalInformationStates.LAST_NAME_PROCESS, "default")
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, PersonalInformationStates.LAST_NAME_PROCESS, "default", next_state, message)
    else:
        invalid_message = data.invalid_messages.invalid_full_name
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = PersonalInformationStates.LAST_NAME
        firebase_service.save_user_state(user_id, next_state)


async def handle_email_state(user_id, data):
    email_message = data.email.messages[0]
    msg = WhatsAppMessage(to=user_id, body=email_message)
    await send_text_message(msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.EMAIL)


async def process_email_response(user_id, message, data, route_to_state_handler):
    user_email = message.text.body
    
    if is_valid_email(user_email):
        firebase_service.save_user_data(user_id, {"email": utils.encrypt(user_email)})
        next_state = get_next_state(PersonalInformationStates.EMAIL_PROCESS, "default")
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, PersonalInformationStates.EMAIL_PROCESS, "default", next_state, message)
    
    else:
        invalid_message = data.invalid_messages.invalid_email
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = PersonalInformationStates.EMAIL
        firebase_service.save_user_state(user_id, next_state)


async def handle_location_country_state(user_id, data):
    location_country_message = data.invalid_messages.country_request_message
    msg = WhatsAppMessage(to=user_id, body=location_country_message)
    await send_text_message(msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.LOCATION_COUNTRY)


async def process_location_country_response(user_id, message, data, route_to_state_handler):
    user_location_country = message.text.body
    valid_countries = get_countries().valid_countries
    
    if is_valid_country(user_location_country, valid_countries):
        country = utils.get_country_by_name(user_location_country, valid_countries)
        firebase_service.save_user_data(user_id, {"country_data": country.name,
                                                  "country_code": country.alpha_code})
        next_state = get_next_state(PersonalInformationStates.LOCATION_COUNTRY_PROCESS, "valid_response")
    else:
        invalid_message = data.invalid_messages.invalid_country
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = PersonalInformationStates.LOCATION_COUNTRY
    
    firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, PersonalInformationStates.LOCATION_COUNTRY_PROCESS, "default", next_state, message)


async def handle_location_state(user_id, data):
    location_message = data.location.messages[0]
    location_interactive = data.location.interactive
    msg = WhatsAppMessage(to=user_id, body=location_message)
    await send_text_message(msg)
    interactive_msg = InteractiveMessage(to=user_id, interactive=location_interactive.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.LOCATION)


async def process_location_response(user_id, message, data, route_to_state_handler):
    interactive = data.location.interactive
    user_response_id = message.interactive.list_reply.id
    if not check_valid(user_response_id, interactive):
        await handle_location_state(user_id, data)
    else:
        if user_response_id == 'i_not_in_south_africa':
            next_state = get_next_state(PersonalInformationStates.LOCATION_PROCESS,
                                        "i_not_in_south_africa")
        else:
            next_state = get_next_state(PersonalInformationStates.LOCATION_PROCESS, "default")
            firebase_service.save_user_data(user_id, {"country_data": message.interactive.list_reply.title,
                                                      "country_code": "ZA"})
            firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, PersonalInformationStates.LOCATION_PROCESS, "default", next_state, message)


async def handle_phone_number_state(user_id, data):
    phone_number_message = data.phone_number.messages[0]
    msg = WhatsAppMessage(to=user_id, body=phone_number_message)
    await send_text_message(msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.PHONE_NUMBER)


async def process_phone_number_response(user_id, message, data, route_to_state_handler):
    user_phone_number = message.text.body
    
    if is_valid_phone_number(user_phone_number):
        firebase_service.save_user_data(user_id, {"phone_number": utils.encrypt(user_phone_number)})
        next_state = get_next_state(PersonalInformationStates.PHONE_NUMBER_PROCESS, "default")
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, PersonalInformationStates.PHONE_NUMBER_PROCESS, "default", next_state, message)
    else:
        invalid_message = data.invalid_messages.invalid_phone_number
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = PersonalInformationStates.PHONE_NUMBER
        firebase_service.save_user_state(user_id, next_state)


async def handle_date_of_birth_state(user_id, data):
    date_of_birth_message = data.date_of_birth.messages[0]
    msg = WhatsAppMessage(to=user_id, body=date_of_birth_message)
    await send_text_message(msg)
    firebase_service.save_user_state(user_id, PersonalInformationStates.DATE_OF_BIRTH)


async def process_date_of_birth_response(user_id, message, data, route_to_state_handler):
    user_date_of_birth = message.text.body
    if not is_valid_date_of_birth(user_date_of_birth) or not is_age_valid_range(user_date_of_birth):
        invalid_message = data.invalid_messages.invalid_date_of_birth
        msg = WhatsAppMessage(to=user_id, body=invalid_message)
        await send_text_message(msg)
        next_state = PersonalInformationStates.DATE_OF_BIRTH
        firebase_service.save_user_state(user_id, next_state)
    
    else:
        if is_age_valid_and_18_or_older(user_date_of_birth):
            next_state = get_next_state(PersonalInformationStates.DATE_OF_BIRTH_PROCESS, "default")
            firebase_service.save_user_state(user_id, next_state)
        else:
            next_state = get_next_state(PersonalInformationStates.DATE_OF_BIRTH_MINOR, "default")
            firebase_service.save_user_state(user_id, next_state)
            
        firebase_service.save_user_data(user_id, {"date_of_birth": user_date_of_birth})

    await route_to_state_handler(user_id, PersonalInformationStates.DATE_OF_BIRTH_PROCESS, "default", next_state, message)


async def handle_date_of_birth_minor_response(user_id, message, data, route_to_state_handler):
    guardian_message = data.guardian_authorization_options.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=guardian_message.dict())
    await send_interactive_message(interactive_msg)


async def process_date_of_birth_minor_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    guardian_authorization = data.guardian_authorization_options.interactive
    if not check_valid_interactive(user_response_id, guardian_authorization):
        await handle_date_of_birth_minor_response(user_id, message, data, route_to_state_handler)
        next_state = get_next_state(PersonalInformationStates.DATE_OF_BIRTH_MINOR_PROCESS, "default")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(PersonalInformationStates.DATE_OF_BIRTH_MINOR_PROCESS, user_response_id)
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, PersonalInformationStates.DATE_OF_BIRTH_MINOR_PROCESS, user_response_id, next_state, message)


async def handle_date_of_birth_minor_parent(user_id, message, data, route_to_state_handler):
    authorization_reminder = data.guardian_authorization_reminder_button.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=authorization_reminder.dict())
    await send_interactive_message(interactive_msg)
    next_state = get_next_state(PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT, "default")
    firebase_service.save_user_state(user_id, next_state)


async def process_date_of_birth_minor_parent_response(user_id, message, data, route_to_state_handler):
    if hasattr(message, 'interactive') and message.interactive:
        user_response_id = message.interactive.button_reply.id
    else:
        user_response_id = "default"
    guardian_authorization = data.guardian_authorization_reminder_button.interactive
    if not check_valid_interactive(user_response_id, guardian_authorization):
        await handle_date_of_birth_minor_parent(user_id, message, data, route_to_state_handler)
    else:
        next_state = get_next_state(PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT_PROCESS, user_response_id)
        firebase_service.save_user_state(user_id, next_state)
        await route_to_state_handler(user_id, PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT_PROCESS, user_response_id, next_state, message)
