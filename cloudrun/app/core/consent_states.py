from enum import Enum


class ConsentStates(str, Enum):
    CONSENT_START = "consent_start"
    CONSENT_PROCESS = "consent_process"
    CONSENT_IMAGE_GIVEN = "consent_image"
    CONSENT_IMAGE_REVOKED = "de_consent_image"


CONSENT_STATE_TRANSITIONS = {
    ConsentStates.CONSENT_START: {
        "default": ConsentStates.CONSENT_PROCESS,
    },
    ConsentStates.CONSENT_PROCESS: {
        "default": ConsentStates.CONSENT_PROCESS,
        "consent_image": ConsentStates.CONSENT_PROCESS,
        "de_consent_image": ConsentStates.CONSENT_PROCESS,
    },
    ConsentStates.CONSENT_IMAGE_GIVEN: {
        "default": ConsentStates.CONSENT_IMAGE_GIVEN,
    },
    ConsentStates.CONSENT_IMAGE_REVOKED: {
        "default": ConsentStates.CONSENT_IMAGE_REVOKED,
    },
}
