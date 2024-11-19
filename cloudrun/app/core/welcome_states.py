from enum import Enum

from app.core.personal_information_states import PersonalInformationStates


class WelcomeStates(str, Enum):
    WELCOME_PRIVACY_POLICY = "welcome_privacy_policy"
    STOP = "stop"
    STOP_PROCESS = "stop_process"
    RESTART = "restart"
    I_AGREE = "i_agree"
    I_DISAGREE = "i_disagree"
    I_DISAGREE_PROCESS = "i_disagree_process"
    THANK_YOU = "thank_you"
    SHOW_TERMS_POLICY = "show_terms_policy"
    SHOW_TERMS_POLICY_PROCESS = "show_terms_policy_process"


WELCOME_STATE_TRANSITIONS = {
    WelcomeStates.WELCOME_PRIVACY_POLICY: {
        "default": WelcomeStates.WELCOME_PRIVACY_POLICY,
        "i_agree": WelcomeStates.THANK_YOU,
        "i_disagree": WelcomeStates.I_DISAGREE,
        "show_terms_policy": WelcomeStates.SHOW_TERMS_POLICY
    },
    WelcomeStates.I_DISAGREE: {
        "default": WelcomeStates.I_DISAGREE_PROCESS
    },
    WelcomeStates.I_DISAGREE_PROCESS: {
        "i_stop_here": WelcomeStates.STOP,
        "i_accept": WelcomeStates.THANK_YOU,
        "default": WelcomeStates.I_DISAGREE_PROCESS
    },
    WelcomeStates.THANK_YOU: {
        "default": PersonalInformationStates.SELECT_GENDER
    },
    WelcomeStates.STOP: {
        "default": WelcomeStates.STOP_PROCESS
    },
    WelcomeStates.STOP_PROCESS: {
        "i_reset": WelcomeStates.WELCOME_PRIVACY_POLICY,
        "default": WelcomeStates.STOP_PROCESS
    },
    WelcomeStates.RESTART: WelcomeStates.WELCOME_PRIVACY_POLICY,
    
    WelcomeStates.SHOW_TERMS_POLICY: {
        "default": WelcomeStates.SHOW_TERMS_POLICY_PROCESS,
    },
    WelcomeStates.SHOW_TERMS_POLICY_PROCESS: {
        "default": WelcomeStates.SHOW_TERMS_POLICY_PROCESS,
        "show_policy_privacy_i_agree": WelcomeStates.THANK_YOU,
        "show_policy_privacy_i_disagree": WelcomeStates.I_DISAGREE,
    }
}
