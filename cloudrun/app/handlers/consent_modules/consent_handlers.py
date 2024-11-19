from app.constants import Constants
from app.core.consent_states import ConsentStates
from app.model.data_flow_extend import DataFlowExtend
from app.services.firebase import FirebaseService
from app.schemas.whatsapp.message import WhatsAppMessage, InteractiveMessage
from app.services.message_service import send_interactive_message
from app.utils.state_utils import get_next_state
from app.utils.helpers import Helpers


firebase_service = FirebaseService()
utils = Helpers()


async def handle_consent_start(user_id, data):
    consent_start_message = data.consent_data_image.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=consent_start_message.dict())
    await send_interactive_message(interactive_msg)
    data_flow_extend = DataFlowExtend(
        flow_extend=True,
        name_flow_extend=ConsentStates.CONSENT_PROCESS
    )
    firebase_service.save_user_data(user_id, data_flow_extend.dict(by_alias=True))


async def handle_consent_process(user_id, message, data, route_to_state_handler):
    user_response_id = message.interactive.button_reply.id
    if user_response_id == "consent_image":
        utils.set_consent_action(user_id, Constants.ACTION_TYPE_CONSENT)
    else:
        utils.set_consent_action(user_id, Constants.ACTION_TYPE_DE_CONSENT)
    
    data_flow_extend = DataFlowExtend(
        flow_extend=False,
        name_flow_extend=""
    )
    firebase_service.save_user_data(user_id, data_flow_extend.dict(by_alias=True))
    current_state = firebase_service.get_user_state(user_id)
    await route_to_state_handler(user_id, current_state, user_response_id, current_state, message)
