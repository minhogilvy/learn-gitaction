import asyncio

from app.core.data_loader import get_data
from app.core.questions_states import QuestionStates
from app.schemas.whatsapp.message import InteractiveMessage, WhatsAppMessage
from app.services.firebase import FirebaseService
from app.services.message_service import send_interactive_message, send_text_message
from app.utils.calculate_score import OralHealthScoreCalculator
from app.utils.helpers import Helpers
from app.utils.state_utils import get_next_state
from app.utils.validators import check_valid


firebase_service = FirebaseService()
utils = Helpers()
calculator = OralHealthScoreCalculator()


async def handle_question_frequency_of_pain_in_teeth_or_gums(user_id, data):
    question = data.frequency_of_pain_in_teeth_or_gums.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=question.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS)


async def process_question_frequency_of_pain_in_teeth_or_gums_response(user_id, message, data, route_to_state_handler):
    user_response_id = get_user_response_id(message)
    user_response_title = get_user_response_title(message)
    interactive = data.frequency_of_pain_in_teeth_or_gums.interactive
    if not check_valid(user_response_id, interactive):
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS_PROCESS, "default")
        score = calculator.get_score_by_quest_id(user_response_id)
        firebase_service.set_user_score(user_id, score)
        firebase_service.save_user_data(user_id, {"answer_for_question_1": user_response_title})
        firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS_PROCESS, user_response_id, next_state, message)


async def handle_question_frequency_of_bleeding_gums(user_id, data):
    question = data.frequency_of_bleeding_gums.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=question.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, QuestionStates.FREQUENCY_OF_BLEEDING_GUMS)


async def process_question_frequency_of_bleeding_gums_response(user_id, message, data, route_to_state_handler):
    user_response_id = get_user_response_id(message)
    user_response_title = get_user_response_title(message)
    interactive = data.frequency_of_bleeding_gums.interactive
    if not check_valid(user_response_id, interactive):
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_BLEEDING_GUMS_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_BLEEDING_GUMS_PROCESS, "default")
        score = calculator.get_score_by_quest_id(user_response_id)
        firebase_service.set_user_score(user_id, score)
        firebase_service.save_user_data(user_id, {"answer_for_question_2": user_response_title})
        firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, QuestionStates.FREQUENCY_OF_BLEEDING_GUMS_PROCESS, user_response_id, next_state, message)


async def handle_question_loose_or_moving_teeth(user_id, data):
    question = data.loose_or_moving_teeth.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=question.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, QuestionStates.LOOSE_OR_MOVING_TEETH)


async def process_question_loose_or_moving_teeth_response(user_id, message, data, route_to_state_handler):
    user_response_id = get_user_response_id(message)
    user_response_title = get_user_response_title(message)
    interactive = data.loose_or_moving_teeth.interactive
    if not check_valid(user_response_id, interactive):
        next_state = get_next_state(QuestionStates.LOOSE_OR_MOVING_TEETH_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(QuestionStates.LOOSE_OR_MOVING_TEETH_PROCESS, "default")
        score = calculator.get_score_by_quest_id(user_response_id)
        firebase_service.set_user_score(user_id, score)
        firebase_service.save_user_data(user_id, {"answer_for_question_3": user_response_title})
        firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, QuestionStates.LOOSE_OR_MOVING_TEETH_PROCESS, user_response_id, next_state, message)


async def handle_question_frequency_of_brushing_teeth(user_id, data):
    question = data.frequency_of_brushing_teeth.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=question.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, QuestionStates.FREQUENCY_OF_BRUSHING_TEETH)


async def process_question_frequency_of_brushing_teeth_response(user_id, message, data, route_to_state_handler):
    user_response_id = get_user_response_id(message)
    user_response_title = get_user_response_title(message)
    interactive = data.frequency_of_brushing_teeth.interactive
    if not check_valid(user_response_id, interactive):
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_BRUSHING_TEETH_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_BRUSHING_TEETH_PROCESS, "default")
        score = calculator.get_score_by_quest_id(user_response_id)
        firebase_service.set_user_score(user_id, score)
        firebase_service.save_user_data(user_id, {"answer_for_question_4": user_response_title})
        firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, QuestionStates.FREQUENCY_OF_BRUSHING_TEETH_PROCESS, user_response_id, next_state, message)


async def handle_question_frequency_of_sugar_consumption(user_id, data):
    question = data.frequency_of_sugar_consumption.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=question.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION)


async def process_question_frequency_of_sugar_consumption_response(user_id, message, data, route_to_state_handler):
    user_response_id = get_user_response_id(message)
    user_response_title = get_user_response_title(message)
    interactive = data.frequency_of_sugar_consumption.interactive
    if not check_valid(user_response_id, interactive):
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION_PROCESS, "default")
        score = calculator.get_score_by_quest_id(user_response_id)
        firebase_service.set_user_score(user_id, score)
        firebase_service.save_user_data(user_id, {"answer_for_question_5": user_response_title})
        firebase_service.save_user_state(user_id, next_state)
    await route_to_state_handler(user_id, QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION_PROCESS, user_response_id, next_state, message)


async def handle_question_smoking_habits(user_id, data):
    question = data.smoking_habits.interactive
    interactive_msg = InteractiveMessage(to=user_id, interactive=question.dict())
    await send_interactive_message(interactive_msg)
    firebase_service.save_user_state(user_id, QuestionStates.SMOKING_HABITS)


async def process_question_smoking_habits_response(user_id, message, data, route_to_state_handler):
    user_response_id = get_user_response_id(message)
    user_response_title = get_user_response_title(message)
    interactive = data.smoking_habits.interactive
    if not check_valid(user_response_id, interactive):
        next_state = get_next_state(QuestionStates.SMOKING_HABITS_PROCESS, "invalid_response")
        firebase_service.save_user_state(user_id, next_state)
    else:
        next_state = get_next_state(QuestionStates.SMOKING_HABITS_PROCESS, "default")
        score = calculator.get_score_by_quest_id(user_response_id)
        firebase_service.set_user_score(user_id, score)
        firebase_service.save_user_data(user_id, {"answer_for_question_6": user_response_title, "answered_date": utils.get_date(), "report_url": ""})
        firebase_service.save_user_state(user_id, next_state)
        data_firebase = firebase_service.get_user_data(user_id)
        if data_firebase.get("gemini_data"):
            session_id = firebase_service.get_latest_session_id_by_phone(user_id)
            utils.generate_report(user_id, session_id)
    await route_to_state_handler(user_id, QuestionStates.SMOKING_HABITS_PROCESS, user_response_id, next_state, message)


def get_user_response_id(message):
    if hasattr(message, 'interactive') and message.interactive:
        return message.interactive.list_reply.id


def get_user_response_title(message):
    if hasattr(message, 'interactive') and message.interactive:
        return message.interactive.list_reply.title
