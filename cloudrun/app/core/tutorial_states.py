from enum import Enum

from app.core.dental_analysis_states import DentalAnalysisStates


class TutorialStates(str, Enum):
    START_TUTORIAL = "start_tutorial"
    WATCH_TUTORIAL_PROMPT = "watch_tutorial_prompt"
    VIEW_TUTORIAL_CHECK = "view_tutorial_check"
    VIEW_TUTORIAL_CHECK_PROCESS = "view_tutorial_check_process"
    VIEW_TUTORIAL_YES_ALL_GOOD = "view_tutorial_yes_all_good"
    VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS = "view_tutorial_yes_all_good_process"
    PROCEED_PROMPT = "proceed_prompt"
    READY_PROMPT = "ready_prompt"


TUTORIAL_STATE_TRANSITIONS = {
    TutorialStates.START_TUTORIAL: {
        "watch_the_tutorial": TutorialStates.VIEW_TUTORIAL_CHECK,
        "no_thanks": DentalAnalysisStates.START
    },
    TutorialStates.VIEW_TUTORIAL_CHECK: {
        "default": TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS,
        "yes_all_good": TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS,
        "no_i_wasnt_able_to": TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS,
    },
    TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS: {
        "default": TutorialStates.VIEW_TUTORIAL_CHECK_PROCESS,
        "yes_all_good": TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD,
        "no_i_wasnt_able_to": DentalAnalysisStates.START,
    },
    TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD: {
        "default": TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS,
        "sure": TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS,
        "yes_all_good": TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS,
        "not_yet": TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS
    },
    TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS: {
        "default": TutorialStates.VIEW_TUTORIAL_YES_ALL_GOOD_PROCESS,
        "sure": DentalAnalysisStates.START,
        "not_yet": TutorialStates.READY_PROMPT
    },
    TutorialStates.READY_PROMPT: {
        "im_ready": DentalAnalysisStates.START
    }
}
