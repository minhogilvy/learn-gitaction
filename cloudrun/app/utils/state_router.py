from app.core.consent_states import ConsentStates
from app.core.data_loader import get_data, get_data_questions, get_data_reports
from app.core.feedback_rating_states import FeedbackRatingStates
from app.core.help_states import HelpStates
from app.core.questions_states import QuestionStates
from app.core.reports_states import ReportsStates
from app.core.welcome_states import WelcomeStates
from app.core.personal_information_states import PersonalInformationStates
from app.core.tutorial_states import TutorialStates
from app.core.dental_analysis_states import DentalAnalysisStates
from app.handlers.consent_modules.consent_handlers import handle_consent_start, handle_consent_process
from app.handlers.feedback_rating_modules.feedback_rating_handlers import (
    handle_feedback_rating_start,
    handle_feedback_rating_start_process,
    handle_feedback_rating_yes_sure,
    handle_feedback_rating_no_thanks,
    handle_feedback_rating_excellent,
    handle_feedback_rating_poor,
    process_feedback_rating_poor_process,
    handle_feedback_rating_poor_invalid,
    process_feedback_rating_poor_invalid_process,
    handle_feedback_rating_yes_sure_process,
    handle_feedback_rating_no_thanks_process,
    handle_feedback_rating_start_conversation, handle_feedback_rating_poor_valid
)
from app.handlers.help_modules.help_handlers import (
    handle_help_start,
    process_help_start_response,
    handle_help_make_new_assessment,
    handle_help_more_about_oral_care,
    process_help_make_new_assessment_response,
    process_help_more_about_oral_care_response,
    handle_help_nothing_thats_all,
    handle_help_for_someone_else,
    handle_help_keep_my_data,
    handle_help_no,
    handle_help_yes_do_it,
    handle_help_create_report_again, process_help_create_report_again_process_response
)
from app.handlers.questions_modules.questions_handler import (
    handle_question_frequency_of_pain_in_teeth_or_gums,
    process_question_frequency_of_pain_in_teeth_or_gums_response,
    handle_question_frequency_of_bleeding_gums,
    process_question_frequency_of_bleeding_gums_response,
    handle_question_loose_or_moving_teeth,
    process_question_loose_or_moving_teeth_response,
    handle_question_frequency_of_brushing_teeth,
    process_question_frequency_of_brushing_teeth_response,
    handle_question_frequency_of_sugar_consumption,
    process_question_frequency_of_sugar_consumption_response,
    handle_question_smoking_habits,
    process_question_smoking_habits_response
)
from app.handlers.reports_modules.reports_handlers import (
    handle_reports_start,
    handle_reports_start_process,
    handle_report_invalid,
    process_report_invalid_process,
    handle_report_invalid_again,
    handle_report_valid, handle_report_valid_message,
)
from app.handlers.welcome_modules.welcome_handle import (
    handle_welcome_privacy_policy_state,
    handle_i_agree_state,
    handle_i_disagree_state,
    handle_thank_you_state,
    handle_stop_state,
    handle_restart_state,
    handle_show_terms_policy_state, process_show_terms_policy_response, handle_i_disagree_process_state, handle_stop_process_state,
)
from app.handlers.information_modules.information_handler import (
    handle_gender_state,
    process_gender_response,
    handle_email_state,
    process_email_response,
    handle_location_state,
    process_location_response,
    handle_phone_number_state,
    process_phone_number_response,
    handle_date_of_birth_state,
    process_date_of_birth_response,
    handle_location_country_state,
    process_location_country_response,
    handle_first_name_state,
    process_first_name_response,
    handle_last_name_state,
    process_last_name_response, handle_date_of_birth_minor_parent, process_date_of_birth_minor_response, process_date_of_birth_minor_parent_response,
)

from app.handlers.tutorial_modules.tutorial_handler import (
    handle_start_tutorial,
    handle_view_tutorial_check,
    process_view_tutorial_check_response,
    process_proceed_prompt_response,
    process_ready_prompt_response, handle_watch_tutorial_prompt, handle_view_tutorial_yes_all_good_check, process_view_tutorial_yes_all_good_process_response,

)
from app.handlers.dental_analysis_modules.dental_analysis_handler import (
    handle_dental_analysis,
    handle_lower_teeth_prompt,
    process_lower_teeth_response,
    handle_upper_teeth_prompt,
    process_upper_teeth_response,
    handle_front_teeth_prompt,
    process_front_teeth_response,
    handle_thank_you_analyze,
    process_thank_you_analyze_response,
    handle_ready_prompt,
    handle_thank_you_analyze_not_now_response,
    process_thank_you_analyze_not_now_response
)


async def route_to_state_handler(user_id, current_state, user_response_id, next_state, message, background_tasks=None):
    data = get_data()
    data_questions = get_data_questions()
    data_reports = get_data_reports()
    if next_state in WelcomeStates.__members__.values():
        await route_welcome_states(user_id, current_state, user_response_id, next_state, message, data)
    elif next_state in PersonalInformationStates.__members__.values():
        await route_personal_information_states(user_id, current_state, user_response_id, next_state, message, data)
    elif next_state in TutorialStates.__members__.values():
        await route_tutorial_states(user_id, current_state, user_response_id, next_state, message, data)
    elif next_state in DentalAnalysisStates.__members__.values():
        await route_dental_analysis_states(user_id, current_state, user_response_id, next_state, message, data, background_tasks)
    elif next_state in QuestionStates.__members__.values():
        await route_question_states(user_id, current_state, user_response_id, next_state, message, data_questions)
    elif next_state in ReportsStates.__members__.values():
        await route_reports_states(user_id, current_state, user_response_id, next_state, message, data_reports)
    elif next_state in HelpStates.__members__.values():
        await route_help_states(user_id, current_state, user_response_id, next_state, message, data_reports, data)
    elif next_state in FeedbackRatingStates.__members__.values():
        await route_feedback_rating_states(user_id, current_state, user_response_id, next_state, message, data_reports, background_tasks)
    elif next_state in ConsentStates.__members__.values():
        await route_consent_states(user_id, current_state, user_response_id, next_state, message, data, background_tasks)


async def route_welcome_states(user_id, current_state, user_response_id, next_state, message, data):
    if next_state == WelcomeStates.WELCOME_PRIVACY_POLICY:
        await handle_welcome_privacy_policy_state(user_id)
    elif next_state == WelcomeStates.I_AGREE:
        await handle_i_agree_state(user_id)
    elif next_state == WelcomeStates.I_DISAGREE:
        await handle_i_disagree_state(user_id)
    elif next_state == WelcomeStates.I_DISAGREE_PROCESS:
        await handle_i_disagree_process_state(user_id, message, data, route_to_state_handler)
    elif next_state == WelcomeStates.THANK_YOU:
        await handle_thank_you_state(user_id, data.thank_you, data, route_to_state_handler)
    elif next_state == WelcomeStates.STOP:
        await handle_stop_state(user_id)
    elif next_state == WelcomeStates.STOP_PROCESS:
        await handle_stop_process_state(user_id, data.thank_you, data, route_to_state_handler)
    elif next_state == WelcomeStates.RESTART:
        await handle_restart_state(user_id)
    elif next_state == WelcomeStates.SHOW_TERMS_POLICY:
        await handle_show_terms_policy_state(user_id)
    elif next_state == WelcomeStates.SHOW_TERMS_POLICY_PROCESS:
        await process_show_terms_policy_response(user_id, message, data, route_to_state_handler)


async def route_personal_information_states(user_id, current_state, user_response_id, next_state, message, data):
    if next_state == PersonalInformationStates.THANK_YOU:
        await handle_thank_you_state(user_id, data.thank_you, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.SELECT_GENDER:
        await handle_gender_state(user_id, data)
    elif next_state == PersonalInformationStates.SELECT_GENDER_PROCESS:
        await process_gender_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.FIRST_NAME:
        await handle_first_name_state(user_id, data)
    elif next_state == PersonalInformationStates.FIRST_NAME_PROCESS:
        await process_first_name_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.LAST_NAME:
        await handle_last_name_state(user_id, data)
    elif next_state == PersonalInformationStates.LAST_NAME_PROCESS:
        await process_last_name_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.EMAIL:
        await handle_email_state(user_id, data)
    elif next_state == PersonalInformationStates.EMAIL_PROCESS:
        await process_email_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.LOCATION:
        await handle_location_state(user_id, data)
    elif next_state == PersonalInformationStates.LOCATION_PROCESS:
        await process_location_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.PHONE_NUMBER:
        await handle_phone_number_state(user_id, data)
    elif next_state == PersonalInformationStates.PHONE_NUMBER_PROCESS:
        await process_phone_number_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.DATE_OF_BIRTH:
        await handle_date_of_birth_state(user_id, data)
    elif next_state == PersonalInformationStates.DATE_OF_BIRTH_PROCESS:
        await process_date_of_birth_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.DATE_OF_BIRTH_MINOR_PROCESS:
        await process_date_of_birth_minor_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT:
        await handle_date_of_birth_minor_parent(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT_PROCESS:
        await process_date_of_birth_minor_parent_response(user_id, message, data, route_to_state_handler)
    elif next_state == PersonalInformationStates.LOCATION_COUNTRY:
        await handle_location_country_state(user_id, data)
    elif next_state == PersonalInformationStates.LOCATION_COUNTRY_PROCESS:
        await process_location_country_response(user_id, message, data, route_to_state_handler)


async def route_tutorial_states(user_id, current_state, user_response_id, next_state, message, data):
    if next_state == TutorialStates.START_TUTORIAL:
        await handle_start_tutorial(user_id, data)
    elif next_state == TutorialStates.WATCH_TUTORIAL_PROMPT:
        await handle_watch_tutorial_prompt(user_id, data)
    elif next_state == TutorialStates.VIEW_TUTORIAL_CHECK:
        await handle_view_tutorial_check(user_id, data)
    elif next_state == TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS:
        await process_view_tutorial_check_response(user_id, message, data, route_to_state_handler)
    elif next_state == TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD:
        await handle_view_tutorial_yes_all_good_check(user_id, data)
    elif next_state == TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS:
        await process_view_tutorial_yes_all_good_process_response(user_id, message, data, route_to_state_handler)
    elif next_state == TutorialStates.PROCEED_PROMPT:
        await process_proceed_prompt_response(user_id, message, data, route_to_state_handler)
    elif next_state == TutorialStates.READY_PROMPT:
        await process_ready_prompt_response(user_id, message, data, route_to_state_handler)


async def route_dental_analysis_states(user_id, current_state, user_response_id, next_state, message, data, background_tasks):
    if next_state == DentalAnalysisStates.START:
        await handle_dental_analysis(user_id, data)
    elif next_state == DentalAnalysisStates.LOWER_TEETH_PROMPT:
        await handle_lower_teeth_prompt(user_id, message, data, route_to_state_handler)
    elif next_state == DentalAnalysisStates.LOWER_TEETH_PROMPT_PROCESS:
        await process_lower_teeth_response(user_id, message, data, route_to_state_handler, background_tasks)
    elif next_state == DentalAnalysisStates.READY_PROMPT:
        await handle_ready_prompt(user_id, message, data, route_to_state_handler)
    elif next_state == DentalAnalysisStates.UPPER_TEETH_PROMPT:
        await handle_upper_teeth_prompt(user_id, message, data, route_to_state_handler)
    elif next_state == DentalAnalysisStates.UPPER_TEETH_PROMPT_PROCESS:
        await process_upper_teeth_response(user_id, message, data, route_to_state_handler, background_tasks)
    elif next_state == DentalAnalysisStates.FRONT_TEETH_PROMPT:
        await handle_front_teeth_prompt(user_id, message, data, route_to_state_handler)
    elif next_state == DentalAnalysisStates.FRONT_TEETH_PROMPT_PROCESS:
        await process_front_teeth_response(user_id, message, data, route_to_state_handler, background_tasks)
    elif next_state == DentalAnalysisStates.THANK_YOU_ANALYZE:
        await handle_thank_you_analyze(user_id, data)
    elif next_state == DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW:
        await handle_thank_you_analyze_not_now_response(user_id, message, data)
    elif next_state == DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW_PROCESS:
        await process_thank_you_analyze_not_now_response(user_id, message, data, route_to_state_handler)
    elif next_state == DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS:
        await process_thank_you_analyze_response(user_id, message, data, route_to_state_handler)


async def route_question_states(user_id, current_state, user_response_id, next_state, message, data):
    if next_state == QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS:
        await handle_question_frequency_of_pain_in_teeth_or_gums(user_id, data)
    elif next_state == QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS_PROCESS:
        await process_question_frequency_of_pain_in_teeth_or_gums_response(user_id, message, data, route_to_state_handler)
    elif next_state == QuestionStates.FREQUENCY_OF_BLEEDING_GUMS:
        await handle_question_frequency_of_bleeding_gums(user_id, data)
    elif next_state == QuestionStates.FREQUENCY_OF_BLEEDING_GUMS_PROCESS:
        await process_question_frequency_of_bleeding_gums_response(user_id, message, data, route_to_state_handler)
    elif next_state == QuestionStates.LOOSE_OR_MOVING_TEETH:
        await handle_question_loose_or_moving_teeth(user_id, data)
    elif next_state == QuestionStates.LOOSE_OR_MOVING_TEETH_PROCESS:
        await process_question_loose_or_moving_teeth_response(user_id, message, data, route_to_state_handler)
    elif next_state == QuestionStates.FREQUENCY_OF_BRUSHING_TEETH:
        await handle_question_frequency_of_brushing_teeth(user_id, data)
    elif next_state == QuestionStates.FREQUENCY_OF_BRUSHING_TEETH_PROCESS:
        await process_question_frequency_of_brushing_teeth_response(user_id, message, data, route_to_state_handler)
    elif next_state == QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION:
        await handle_question_frequency_of_sugar_consumption(user_id, data)
    elif next_state == QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION_PROCESS:
        await process_question_frequency_of_sugar_consumption_response(user_id, message, data, route_to_state_handler)
    elif next_state == QuestionStates.SMOKING_HABITS:
        await handle_question_smoking_habits(user_id, data)
    elif next_state == QuestionStates.SMOKING_HABITS_PROCESS:
        await process_question_smoking_habits_response(user_id, message, data, route_to_state_handler)


async def route_reports_states(user_id, current_state, user_response_id, next_state, message, data):
    if next_state == ReportsStates.REPORT_START:
        await handle_reports_start(user_id, data)
    elif next_state == ReportsStates.REPORT_START_PROCESS:
        await handle_reports_start_process(user_id, message, data, route_to_state_handler)
    elif next_state == ReportsStates.REPORT_INVALID:
        await handle_report_invalid(user_id, data)
    elif next_state == ReportsStates.REPORT_INVALID_PROCESS:
        await process_report_invalid_process(user_id, message, data, route_to_state_handler)
    elif next_state == ReportsStates.REPORT_INVALID_AGAIN:
        await handle_report_invalid_again(user_id, data)
    elif next_state == ReportsStates.REPORT_VALID:
        await handle_report_valid(user_id, data)
    elif next_state == ReportsStates.REPORT_VALID_MESSAGE:
        await handle_report_valid_message(user_id, data)


async def route_help_states(user_id, current_state, user_response_id, next_state, message, data, data_dental_analysis):
    if next_state == HelpStates.HELP_START:
        await handle_help_start(user_id, data)
    elif next_state == HelpStates.HELP_START_PROCESS:
        await process_help_start_response(user_id, message, data, route_to_state_handler)
    elif next_state == HelpStates.HELP_MAKE_NEW_ASSESSMENT:
        await handle_help_make_new_assessment(user_id, data)
    elif next_state == HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS:
        await process_help_make_new_assessment_response(user_id, message, data, route_to_state_handler)
    elif next_state == HelpStates.HELP_MORE_ABOUT_ORAL_CARE:
        await handle_help_more_about_oral_care(user_id, data)
    elif next_state == HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS:
        await process_help_more_about_oral_care_response(user_id, message, data, route_to_state_handler)
    elif next_state == HelpStates.HELP_KEEP_MY_DATA:
        await handle_help_keep_my_data(user_id, data, route_to_state_handler)
    elif next_state == HelpStates.HELP_CREATE_REPORT_AGAIN:
        await handle_help_create_report_again(user_id, data)
    elif next_state == HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS:
        await process_help_create_report_again_process_response(user_id, message, data, route_to_state_handler)
    elif next_state == HelpStates.HELP_YES_DO_IT:
        await handle_help_yes_do_it(user_id, data, data_dental_analysis)
    elif next_state == HelpStates.HELP_NO:
        await handle_help_no(user_id, data)
    elif next_state == HelpStates.HELP_NOTHING_THATS_ALL:
        await handle_help_nothing_thats_all(user_id, data, route_to_state_handler)
    elif next_state == HelpStates.HELP_FOR_SOMEONE_ELSE:
        await handle_help_for_someone_else(user_id, data, route_to_state_handler)


async def route_feedback_rating_states(user_id, current_state, user_response_id, next_state, message, data, background_tasks):
    if next_state == FeedbackRatingStates.FEEDBACK_RATING_START:
        await handle_feedback_rating_start(user_id, data)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS:
        await handle_feedback_rating_start_process(user_id, message, data, route_to_state_handler)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_YES_SURE:
        await handle_feedback_rating_yes_sure(user_id, data)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS:
        await handle_feedback_rating_yes_sure_process(user_id, message, data, route_to_state_handler)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS:
        await handle_feedback_rating_no_thanks(user_id, data)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS_PROCESS:
        await handle_feedback_rating_no_thanks_process(user_id, message, data, route_to_state_handler)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_EXCELLENT:
        await handle_feedback_rating_excellent(user_id, data)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_POOR:
        await handle_feedback_rating_poor(user_id, data)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_POOR_PROCESS:
        await process_feedback_rating_poor_process(user_id, message, data, route_to_state_handler)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID:
        await handle_feedback_rating_poor_invalid(user_id, data)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID_PROCESS:
        await process_feedback_rating_poor_invalid_process(user_id, message, data, route_to_state_handler)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_START_CONVERSATION:
        await handle_feedback_rating_start_conversation(user_id, message, data, route_to_state_handler)
    elif next_state == FeedbackRatingStates.FEEDBACK_RATING_POOR_VALID:
        await handle_feedback_rating_poor_valid(user_id, message, data, route_to_state_handler)


async def route_consent_states(user_id, current_state, user_response_id, next_state, message, data, background_tasks):
    if next_state == ConsentStates.CONSENT_START:
        await handle_consent_start(user_id, data)
    elif next_state == ConsentStates.CONSENT_PROCESS:
        await handle_consent_process(user_id, message, data, route_to_state_handler)
