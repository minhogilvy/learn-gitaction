from enum import Enum

from app.core.reports_states import ReportsStates


class QuestionStates(str, Enum):
    FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS = "frequency_of_pain_in_teeth_or_gums"
    FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS_PROCESS = "frequency_of_pain_in_teeth_or_gums_process"
    FREQUENCY_OF_BLEEDING_GUMS = "frequency_of_bleeding_gums"
    FREQUENCY_OF_BLEEDING_GUMS_PROCESS = "frequency_of_bleeding_gums_process"
    LOOSE_OR_MOVING_TEETH = "loose_or_moving_teeth"
    LOOSE_OR_MOVING_TEETH_PROCESS = "loose_or_moving_teeth_process"
    FREQUENCY_OF_BRUSHING_TEETH = "frequency_of_brushing_teeth"
    FREQUENCY_OF_BRUSHING_TEETH_PROCESS = "frequency_of_brushing_teeth_process"
    FREQUENCY_OF_SUGAR_CONSUMPTION = "frequency_of_sugar_consumption"
    FREQUENCY_OF_SUGAR_CONSUMPTION_PROCESS = "frequency_of_sugar_consumption_process"
    SMOKING_HABITS = "smoking_habits"
    SMOKING_HABITS_PROCESS = "smoking_habits_process"


QUESTION_STATE_TRANSITIONS = {
    QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS: {
        "default": QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS_PROCESS
    },
    QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS_PROCESS: {
        "default": QuestionStates.FREQUENCY_OF_BLEEDING_GUMS,
        "invalid_response": QuestionStates.FREQUENCY_OF_PAIN_IN_TEETH_OR_GUMS,
    },
    QuestionStates.FREQUENCY_OF_BLEEDING_GUMS: {
        "default": QuestionStates.FREQUENCY_OF_BLEEDING_GUMS_PROCESS
    },
    QuestionStates.FREQUENCY_OF_BLEEDING_GUMS_PROCESS: {
        "default": QuestionStates.LOOSE_OR_MOVING_TEETH,
        "invalid_response": QuestionStates.FREQUENCY_OF_BLEEDING_GUMS,
    },
    QuestionStates.LOOSE_OR_MOVING_TEETH: {
        "default": QuestionStates.LOOSE_OR_MOVING_TEETH_PROCESS
    },
    QuestionStates.LOOSE_OR_MOVING_TEETH_PROCESS: {
        "default": QuestionStates.FREQUENCY_OF_BRUSHING_TEETH,
        "invalid_response": QuestionStates.LOOSE_OR_MOVING_TEETH,
    },
    QuestionStates.FREQUENCY_OF_BRUSHING_TEETH: {
        "default": QuestionStates.FREQUENCY_OF_BRUSHING_TEETH_PROCESS
    },
    QuestionStates.FREQUENCY_OF_BRUSHING_TEETH_PROCESS: {
        "default": QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION,
        "invalid_response": QuestionStates.FREQUENCY_OF_BRUSHING_TEETH,
    },
    QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION: {
        "default": QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION_PROCESS
    },
    QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION_PROCESS: {
        "default": QuestionStates.SMOKING_HABITS,
        "invalid_response": QuestionStates.FREQUENCY_OF_SUGAR_CONSUMPTION,
    
    },
    QuestionStates.SMOKING_HABITS: {
        "default": QuestionStates.SMOKING_HABITS_PROCESS
    },
    QuestionStates.SMOKING_HABITS_PROCESS: {
        "default": ReportsStates.REPORT_START,
        "invalid_response": QuestionStates.SMOKING_HABITS,
    }
}
