from enum import Enum

from app.core.feedback_rating_states import FeedbackRatingStates


class HelpStates(str, Enum):
    HELP_START = "help_start"
    HELP_START_PROCESS = "help_start_process"
    HELP_MAKE_NEW_ASSESSMENT = "help_make_new_assessment"
    HELP_MAKE_NEW_ASSESSMENT_PROCESS = "help_make_new_assessment_process"
    HELP_MORE_ABOUT_ORAL_CARE = "help_more_about_oral_care"
    HELP_MORE_ABOUT_ORAL_CARE_PROCESS = "help_more_about_oral_care_process"
    HELP_NOTHING_THATS_ALL = "help_nothing_thats_all"
    HELP_NOTHING_THATS_ALL_PROCESS = "help_nothing_thats_all_process"
    HELP_KEEP_MY_DATA = "help_keep_my_data"
    HELP_CREATE_REPORT_AGAIN = "help_create_report_again"
    HELP_CREATE_REPORT_AGAIN_PROCESS = "help_create_report_again_process"
    HELP_FOR_SOMEONE_ELSE = "help_for_someone_else"
    HELP_FOR_SOMEONE_ELSE_PROCESS = "help_for_someone_else_process"
    HELP_YES_DO_IT = "help_yes_do_it"
    HELP_NO = "help_no"


HELP_STATE_TRANSITIONS = {
    HelpStates.HELP_START: {
        "default": HelpStates.HELP_START_PROCESS,
        "make_new_assessment": HelpStates.HELP_START_PROCESS,
        "more_about_oral_care": HelpStates.HELP_START_PROCESS,
        "nothing_thats_all": HelpStates.HELP_START_PROCESS
    },
    HelpStates.HELP_START_PROCESS: {
        "default": HelpStates.HELP_START_PROCESS,
        "make_new_assessment": HelpStates.HELP_MAKE_NEW_ASSESSMENT,
        "more_about_oral_care": HelpStates.HELP_MORE_ABOUT_ORAL_CARE,
        "nothing_thats_all": HelpStates.HELP_NOTHING_THATS_ALL
    },
    HelpStates.HELP_MAKE_NEW_ASSESSMENT: {
        "default": HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS,
        "keep_my_data": HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS,
        "create_report_again": HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS,
        "for_someone_else": HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS
    },
    HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS: {
        "default": HelpStates.HELP_MAKE_NEW_ASSESSMENT_PROCESS,
        "keep_my_data": HelpStates.HELP_KEEP_MY_DATA,
        "create_report_again": HelpStates.HELP_CREATE_REPORT_AGAIN,
        "for_someone_else": HelpStates.HELP_FOR_SOMEONE_ELSE
    },
    HelpStates.HELP_KEEP_MY_DATA: {
        "default": HelpStates.HELP_KEEP_MY_DATA,
    },
    HelpStates.HELP_CREATE_REPORT_AGAIN: {
        "default": HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS,
        "help_yes_do_it": HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS,
        "help_no": HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS
    },
    HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS: {
        "default": HelpStates.HELP_CREATE_REPORT_AGAIN_PROCESS,
        "help_yes_do_it": HelpStates.HELP_YES_DO_IT,
        "help_no": HelpStates.HELP_NO
    },
    HelpStates.HELP_FOR_SOMEONE_ELSE: {
        "default": HelpStates.HELP_FOR_SOMEONE_ELSE,
    },
    HelpStates.HELP_MORE_ABOUT_ORAL_CARE: {
        "default": HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS,
        "make_new_assessment": HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS,
        "no_for_now": HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS,
    },
    HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS: {
        "default": HelpStates.HELP_MORE_ABOUT_ORAL_CARE_PROCESS,
        "make_new_assessment": HelpStates.HELP_MAKE_NEW_ASSESSMENT,
        "no_for_now": FeedbackRatingStates.FEEDBACK_RATING_START,
    },
    HelpStates.HELP_NOTHING_THATS_ALL: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_START
    },
}
