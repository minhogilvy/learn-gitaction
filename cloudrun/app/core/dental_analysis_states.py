from enum import Enum
from app.core.questions_states import QuestionStates


class DentalAnalysisStates(str, Enum):
    START = "dental_analysis_start"
    READY_PROMPT = "dental_analysis_ready_prompt"
    READY_PROMPT_PROCESS = "dental_analysis_ready_prompt_process"
    LOWER_TEETH_PROMPT = "dental_analysis_lower_teeth_prompt"
    LOWER_TEETH_PROMPT_PROCESS = "dental_analysis_lower_teeth_prompt_process"
    UPPER_TEETH_PROMPT = "dental_analysis_upper_teeth_prompt"
    UPPER_TEETH_PROMPT_PROCESS = "dental_analysis_upper_teeth_prompt_process"
    FRONT_TEETH_PROMPT = "dental_analysis_front_teeth_prompt"
    FRONT_TEETH_PROMPT_PROCESS = "dental_analysis_front_teeth_prompt_process"
    THANK_YOU_ANALYZE = "dental_analysis_thank_you_analyze"
    THANK_YOU_ANALYZE_PROCESS = "dental_analysis_thank_you_analyze_process"
    THANK_YOU_ANALYZE_NOT_NOW = "thank_you_analyze_not_now"
    THANK_YOU_ANALYZE_NOT_NOW_PROCESS = "thank_you_analyze_not_now_process"


DENTAL_ANALYSIS_STATE_TRANSITIONS = {
    DentalAnalysisStates.START: {
        "yes_ready": DentalAnalysisStates.LOWER_TEETH_PROMPT,
        "no_wait": DentalAnalysisStates.READY_PROMPT
    },
    DentalAnalysisStates.READY_PROMPT: {
        "default": DentalAnalysisStates.READY_PROMPT_PROCESS,
        "yes_ready": DentalAnalysisStates.READY_PROMPT_PROCESS
    },
    DentalAnalysisStates.READY_PROMPT_PROCESS: {
        "yes_ready": DentalAnalysisStates.LOWER_TEETH_PROMPT
    },
    DentalAnalysisStates.LOWER_TEETH_PROMPT: {
        "default": DentalAnalysisStates.LOWER_TEETH_PROMPT_PROCESS
    },
    DentalAnalysisStates.LOWER_TEETH_PROMPT_PROCESS: {
        "default": DentalAnalysisStates.LOWER_TEETH_PROMPT_PROCESS,
        "valid_response": DentalAnalysisStates.UPPER_TEETH_PROMPT,
        "invalid_response": DentalAnalysisStates.LOWER_TEETH_PROMPT
    },
    DentalAnalysisStates.UPPER_TEETH_PROMPT: {
        "default": DentalAnalysisStates.UPPER_TEETH_PROMPT_PROCESS
    },
    DentalAnalysisStates.UPPER_TEETH_PROMPT_PROCESS: {
        "default": DentalAnalysisStates.UPPER_TEETH_PROMPT_PROCESS,
        "valid_response": DentalAnalysisStates.FRONT_TEETH_PROMPT,
        "invalid_response": DentalAnalysisStates.UPPER_TEETH_PROMPT
    },
    DentalAnalysisStates.FRONT_TEETH_PROMPT: {
        "default": DentalAnalysisStates.FRONT_TEETH_PROMPT_PROCESS
    },
    DentalAnalysisStates.FRONT_TEETH_PROMPT_PROCESS: {
        "default": DentalAnalysisStates.FRONT_TEETH_PROMPT_PROCESS,
        "valid_response": DentalAnalysisStates.THANK_YOU_ANALYZE,
        "invalid_response": DentalAnalysisStates.FRONT_TEETH_PROMPT
    },
    DentalAnalysisStates.THANK_YOU_ANALYZE: {
        "default": DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS,
        "sure": DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS,
        "not_now": DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS
    },
    DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS: {
        "default": DentalAnalysisStates.THANK_YOU_ANALYZE_PROCESS,
        "sure": QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS,
        "not_now": DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW
    },
    DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW: {
        "default": DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW_PROCESS,
        "let_continue": DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW_PROCESS
    },
    DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW_PROCESS: {
        "default": DentalAnalysisStates.THANK_YOU_ANALYZE_NOT_NOW_PROCESS,
        "let_continue": QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS
    }
}
