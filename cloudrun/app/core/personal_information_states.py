from enum import Enum

from app.core.tutorial_states import TutorialStates


class PersonalInformationStates(str, Enum):
    THANK_YOU = "thank_you"
    SELECT_GENDER = "select_gender"
    SELECT_GENDER_PROCESS = "select_gender_process"
    FIRST_NAME = "first_name"
    FIRST_NAME_PROCESS = "first_name_process"
    LAST_NAME = "last_name"
    LAST_NAME_PROCESS = "last_name_process"
    EMAIL = "email"
    EMAIL_PROCESS = "email_process"
    LOCATION = "location"
    LOCATION_PROCESS = "location_process"
    PHONE_NUMBER = "phone_number"
    PHONE_NUMBER_PROCESS = "phone_number_process"
    DATE_OF_BIRTH = "date_of_birth"
    DATE_OF_BIRTH_PROCESS = "date_of_birth_process"
    DATE_OF_BIRTH_MINOR = "date_of_birth_minor"
    DATE_OF_BIRTH_MINOR_PROCESS = "date_of_birth_minor_process"
    DATE_OF_BIRTH_MINOR_PARENT = "date_of_birth_minor_parent"
    DATE_OF_BIRTH_MINOR_PARENT_PROCESS = "date_of_birth_minor_parent_process"
    LOCATION_COUNTRY = "location_country"
    LOCATION_COUNTRY_PROCESS = "location_country_process"


PERSONAL_INFORMATION_STATE_TRANSITIONS = {
    PersonalInformationStates.THANK_YOU: {
        "default": PersonalInformationStates.SELECT_GENDER
    },
    PersonalInformationStates.SELECT_GENDER: {
        "default": PersonalInformationStates.SELECT_GENDER_PROCESS,
    },
    PersonalInformationStates.SELECT_GENDER_PROCESS: {
        "valid_response": PersonalInformationStates.FIRST_NAME,
        "invalid_response": PersonalInformationStates.SELECT_GENDER
    },
    PersonalInformationStates.FIRST_NAME: {
        "default": PersonalInformationStates.FIRST_NAME_PROCESS
    },
    PersonalInformationStates.FIRST_NAME_PROCESS: {
        "default": PersonalInformationStates.LAST_NAME
    },
    PersonalInformationStates.LAST_NAME: {
        "default": PersonalInformationStates.LAST_NAME_PROCESS
    },
    PersonalInformationStates.LAST_NAME_PROCESS: {
        "default": PersonalInformationStates.EMAIL
    },
    PersonalInformationStates.EMAIL: {
        "default": PersonalInformationStates.EMAIL_PROCESS
    },
    PersonalInformationStates.EMAIL_PROCESS: {
        "default": PersonalInformationStates.LOCATION
    },
    PersonalInformationStates.LOCATION: {
        "default": PersonalInformationStates.LOCATION_PROCESS,
        "i_not_in_south_africa": PersonalInformationStates.LOCATION_COUNTRY
    },
    PersonalInformationStates.LOCATION_PROCESS: {
        "default": PersonalInformationStates.PHONE_NUMBER,
        
    },
    PersonalInformationStates.PHONE_NUMBER: {
        "default": PersonalInformationStates.PHONE_NUMBER_PROCESS
    },
    PersonalInformationStates.PHONE_NUMBER_PROCESS: {
        "default": PersonalInformationStates.DATE_OF_BIRTH
    },
    PersonalInformationStates.DATE_OF_BIRTH: {
        "default": PersonalInformationStates.DATE_OF_BIRTH_PROCESS
    },
    PersonalInformationStates.DATE_OF_BIRTH_PROCESS: {
        "default": TutorialStates.START_TUTORIAL
    },
    PersonalInformationStates.DATE_OF_BIRTH_MINOR: {
        "default": PersonalInformationStates.DATE_OF_BIRTH_MINOR_PROCESS,
    },
    PersonalInformationStates.DATE_OF_BIRTH_MINOR_PROCESS: {
        "default": PersonalInformationStates.DATE_OF_BIRTH_MINOR_PROCESS,
        "guardian_authorizes": TutorialStates.START_TUTORIAL,
        "guardian_not_authorized": PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT,
    },
    PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT: {
        "default": PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT_PROCESS,
    },
    PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT_PROCESS: {
        "default": PersonalInformationStates.DATE_OF_BIRTH_MINOR_PARENT_PROCESS,
        "guardian_authorizes": TutorialStates.START_TUTORIAL,
    },
    PersonalInformationStates.LOCATION_COUNTRY: {
        "default": PersonalInformationStates.LOCATION_COUNTRY_PROCESS
    },
    PersonalInformationStates.LOCATION_COUNTRY_PROCESS: {
        "default": PersonalInformationStates.LOCATION_COUNTRY_PROCESS,
        "valid_response": PersonalInformationStates.PHONE_NUMBER,
    }
}
