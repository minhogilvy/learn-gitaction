from enum import Enum

from app.core.feedback_rating_states import FeedbackRatingStates
from app.core.help_states import HelpStates


class ReportsStates(str, Enum):
    REPORT_START = "reports_start"
    REPORT_START_PROCESS = "reports_start_process"
    REPORT_INVALID = "report_invalid"
    REPORT_INVALID_PROCESS = "report_invalid_process"
    REPORT_INVALID_AGAIN = "report_invalid_again"
    REPORT_VALID = "report_valid"
    REPORT_VALID_PROCESS = "report_valid_process"
    REPORT_VALID_MESSAGE = "report_valid_message"



REPORTS_STATE_TRANSITIONS = {
    ReportsStates.REPORT_START: {
        "default": ReportsStates.REPORT_START_PROCESS,
        "valid_response": ReportsStates.REPORT_START_PROCESS,
        "invalid_response": ReportsStates.REPORT_START_PROCESS
    },
    ReportsStates.REPORT_START_PROCESS: {
        "default": ReportsStates.REPORT_START_PROCESS,
        "valid_response": ReportsStates.REPORT_VALID,
        "invalid_response": ReportsStates.REPORT_INVALID
    },
    ReportsStates.REPORT_INVALID: {
        "default": ReportsStates.REPORT_INVALID_PROCESS,
        "valid_response": ReportsStates.REPORT_INVALID_PROCESS,
        "invalid_response": ReportsStates.REPORT_INVALID_PROCESS,
    },
    ReportsStates.REPORT_INVALID_PROCESS: {
        "default": ReportsStates.REPORT_INVALID_PROCESS,
        "valid_response": ReportsStates.REPORT_VALID,
        "invalid_response": ReportsStates.REPORT_INVALID_AGAIN
    },
    ReportsStates.REPORT_INVALID_AGAIN: {
        "default": ReportsStates.REPORT_INVALID,
    },
    ReportsStates.REPORT_VALID: {
        "default": ReportsStates.REPORT_VALID_PROCESS,
        "no_help": ReportsStates.REPORT_VALID_PROCESS,
        "need_help": ReportsStates.REPORT_VALID_PROCESS,
    },
    ReportsStates.REPORT_VALID_MESSAGE: {
        "default": ReportsStates.REPORT_VALID_PROCESS,
        "no_help": ReportsStates.REPORT_VALID_PROCESS,
        "need_help": ReportsStates.REPORT_VALID_PROCESS,
    },
    ReportsStates.REPORT_VALID_PROCESS: {
        "default": ReportsStates.REPORT_VALID_PROCESS,
        "no_help": FeedbackRatingStates.FEEDBACK_RATING_START,
        "need_help": HelpStates.HELP_START,
    }
}
