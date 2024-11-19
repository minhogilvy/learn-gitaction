from app.core.consent_states import CONSENT_STATE_TRANSITIONS, ConsentStates
from app.core.feedback_rating_states import FEEDBACK_RATING_STATE_TRANSITIONS, FeedbackRatingStates
from app.core.help_states import HELP_STATE_TRANSITIONS
from app.core.questions_states import QUESTION_STATE_TRANSITIONS, QuestionStates
from app.core.reports_states import REPORTS_STATE_TRANSITIONS, ReportsStates
from app.core.welcome_states import WELCOME_STATE_TRANSITIONS
from app.core.personal_information_states import PERSONAL_INFORMATION_STATE_TRANSITIONS, PersonalInformationStates
from app.core.tutorial_states import TUTORIAL_STATE_TRANSITIONS
from app.core.dental_analysis_states import DENTAL_ANALYSIS_STATE_TRANSITIONS, DentalAnalysisStates
from app.utils.helpers import Helpers


utils = Helpers()


def get_next_state(current_state, user_response_id):
    if current_state in WELCOME_STATE_TRANSITIONS:
        transitions = WELCOME_STATE_TRANSITIONS.get(current_state, {})
        return transitions.get(user_response_id, transitions.get("default"))
    elif current_state in PERSONAL_INFORMATION_STATE_TRANSITIONS:
        transitions = PERSONAL_INFORMATION_STATE_TRANSITIONS.get(current_state, {})
        return transitions.get(user_response_id, transitions.get("default"))
    elif current_state in TUTORIAL_STATE_TRANSITIONS:
        return TUTORIAL_STATE_TRANSITIONS[current_state].get(user_response_id)
    elif current_state in DENTAL_ANALYSIS_STATE_TRANSITIONS:
        return DENTAL_ANALYSIS_STATE_TRANSITIONS[current_state].get(user_response_id)
    elif current_state in QUESTION_STATE_TRANSITIONS:
        transitions = QUESTION_STATE_TRANSITIONS.get(current_state, {})
        return transitions.get(user_response_id, transitions.get("default"))
    elif current_state in REPORTS_STATE_TRANSITIONS:
        state = get_type_by_state(current_state)
        if state == "text":
            transitions = REPORTS_STATE_TRANSITIONS.get(current_state, {})
            return transitions.get(user_response_id, transitions.get("default"))
        else:
            return REPORTS_STATE_TRANSITIONS[current_state].get(user_response_id)
    elif current_state in HELP_STATE_TRANSITIONS:
        return HELP_STATE_TRANSITIONS[current_state].get(user_response_id)
    elif current_state in FEEDBACK_RATING_STATE_TRANSITIONS:
        state = get_type_by_state(current_state)
        if state == "text":
            transitions = FEEDBACK_RATING_STATE_TRANSITIONS.get(current_state, {})
            return transitions.get(user_response_id, transitions.get("default"))
        else:
            return FEEDBACK_RATING_STATE_TRANSITIONS[current_state].get(user_response_id)
    elif current_state in CONSENT_STATE_TRANSITIONS:
        return CONSENT_STATE_TRANSITIONS[current_state].get(user_response_id)
    else:
        return None


def get_type_by_state(current_state):
    current = utils.check_and_remove_process(current_state)
    if current in [
        PersonalInformationStates.FIRST_NAME,
        PersonalInformationStates.LAST_NAME,
        PersonalInformationStates.EMAIL,
        PersonalInformationStates.PHONE_NUMBER,
        PersonalInformationStates.LOCATION_COUNTRY,
        PersonalInformationStates.DATE_OF_BIRTH,
        ReportsStates.REPORT_START,
        ReportsStates.REPORT_INVALID,
        FeedbackRatingStates.FEEDBACK_RATING_POOR,
        FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID
    ]:
        return "text"
    elif current in [
        PersonalInformationStates.SELECT_GENDER,
        PersonalInformationStates.LOCATION,
        QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS,
        QuestionStates.FREQUENCY_OF_BLEEDING_GUMS,
        QuestionStates.LOOSE_OR_MOVING_TEETH,
        QuestionStates.FREQUENCY_OF_BRUSHING_TEETH,
        QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION,
        QuestionStates.SMOKING_HABITS,
        FeedbackRatingStates.FEEDBACK_RATING_YES_SURE,
    ]:
        return "list_reply"
    else:
        return "button_reply"


def get_type_by_image(current_state):
    current = utils.check_and_remove_process(current_state)
    if current in [
        DentalAnalysisStates.LOWER_TEETH_PROMPT,
        DentalAnalysisStates.FRONT_TEETH_PROMPT,
        DentalAnalysisStates.UPPER_TEETH_PROMPT
    ]:
        return True
    return False


def get_state_flow_extend(current_state):
    current = utils.check_and_remove_process(current_state)
    if current in [
        ConsentStates.CONSENT_START,
        ConsentStates.CONSENT_PROCESS,
        ConsentStates.CONSENT_IMAGE_GIVEN,
        ConsentStates.CONSENT_IMAGE_REVOKED
    ]:
        return True
    return False
