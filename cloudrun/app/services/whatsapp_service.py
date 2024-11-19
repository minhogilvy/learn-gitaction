import datetime
import json
from fastapi import HTTPException
from app.constants import Constants
from app.core.data_loader import get_data
from app.core.welcome_states import WelcomeStates
from app.core.personal_information_states import PersonalInformationStates
from app.handlers.welcome_modules.welcome_handle import handle_welcome_privacy_policy_state
from app.model.data_audit_trail_log import DataAuditTrailLog
from app.schemas.whatsapp.webhooks import WebhookData
from app.schemas.whatsapp.message import WhatsAppMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_text_message
from app.utils.helpers import Helpers
from app.utils.state_utils import get_next_state, get_type_by_state, get_type_by_image, get_state_flow_extend
from app.utils.state_router import route_to_state_handler
from starlette.background import BackgroundTasks


firebase_service = FirebaseService()
utils = Helpers()


async def handle_flow(data: WebhookData, background_tasks: BackgroundTasks):
    for entry in data.entry:
        for change in entry.changes:
            value = change.value
            
            # Process messages
            if value.messages:
                for message in value.messages:
                    await process_message(message, background_tasks)
            
            # Ignore statuses
            if value.statuses:
                print("Ignoring service status messages")


async def process_message(message, background_tasks):
    user_id = utils.encrypt(message.from_)
    
    # Check if user exists
    user_exists = firebase_service.user_exists(user_id)
    user_data = firebase_service.get_user_data(user_id)
    if not user_exists:
        # Create user with default state
        firebase_service.create_user(user_id)
        current_state = WelcomeStates.WELCOME_PRIVACY_POLICY
        message_string = utils.get_message_string(message)
        firebase_service.save_user_history(user_id, message_string, user_id)
        # Send welcome and privacy policy messages immediately after creating the user
        await handle_welcome_privacy_policy_state(user_id)

        return
    else:
        # Load current state from Firestore
        current_state = user_data.get('state')
        
    
    # Determine the user response id based on message type
    if hasattr(message, 'interactive') and message.interactive:
        if message.interactive.button_reply:
            user_response_id = message.interactive.button_reply.id
            if user_data.get('flow_extend') and get_state_flow_extend(user_response_id):
                current_state = user_data.get('name_flow_extend')
        elif message.interactive.list_reply:
            user_response_id = message.interactive.list_reply.id
    elif hasattr(message, 'text') and message.text:
        user_response_id = message.text.body.lower()
        if user_response_id == "!0123456789!":
            firebase_service.create_user(user_id)
            return
        if user_response_id == "@0123456789@":
            firebase_service.save_user_state(user_id, "frequency_of_pain_in_teeth_or_gums")
            return
        if user_response_id == "@consent":
            current_state = Constants.CONSENT_FLOW
            await send_default_message(user_id, current_state, user_response_id, message, background_tasks)
            return
    else:
        user_response_id = "default"

    message_string = utils.get_message_string(message)
    firebase_service.save_user_history(user_id, message_string, user_id)
    # Validate the current state and user response before transitioning
    expected_type = get_type_by_state(current_state)
    skip_state = get_type_by_image(current_state)
    actual_type = message.type
    if message.type == "interactive":
        actual_type = message.interactive.type

    if expected_type != actual_type and not skip_state:
        await send_default_message(user_id, current_state, user_response_id, message, background_tasks)
        return

    # Validate the current state and user response before transitioning
    next_state = get_next_state(current_state, user_response_id)
    if next_state:
        await route_to_state_handler(user_id, current_state, user_response_id, next_state, message, background_tasks)
    else:
        print(f"No valid transition from state '{current_state}' with response '{user_response_id}'")
        # Handle cases where there is no valid state transition
        await send_default_message(user_id, current_state, user_response_id, message, background_tasks)


async def send_default_message(user_id, current_state, user_response_id, message, background_tasks):
    state = utils.check_and_remove_process(current_state)
    await route_to_state_handler(user_id, state, user_response_id, state, message, background_tasks)

