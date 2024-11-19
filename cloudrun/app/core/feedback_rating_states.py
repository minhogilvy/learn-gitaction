from enum import Enum


class FeedbackRatingStates(str, Enum):
    FEEDBACK_RATING_START = "feedback_rating_start"
    FEEDBACK_RATING_START_PROCESS = "feedback_rating_start_process"
    FEEDBACK_RATING_YES_SURE = "feedback_rating_yes_sure"
    FEEDBACK_RATING_YES_SURE_PROCESS = "feedback_rating_yes_sure_process"
    FEEDBACK_RATING_NO_THANKS = "feedback_rating_no_thanks"
    FEEDBACK_RATING_NO_THANKS_PROCESS = "feedback_rating_no_thanks_process"
    FEEDBACK_RATING_START_CONVERSATION = "feedback_rating_start_conversation"
    FEEDBACK_RATING_EXCELLENT = "feedback_rating_excellent"
    FEEDBACK_RATING_POOR = "feedback_rating_poor"
    FEEDBACK_RATING_POOR_PROCESS = "feedback_rating_poor_process"
    FEEDBACK_RATING_POOR_VALID = "feedback_rating_poor_valid"
    FEEDBACK_RATING_POOR_INVALID = "feedback_rating_poor_invalid"
    FEEDBACK_RATING_POOR_INVALID_PROCESS = "feedback_rating_poor_invalid_process"


FEEDBACK_RATING_STATE_TRANSITIONS = {
    FeedbackRatingStates.FEEDBACK_RATING_START: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS,
        "yes_sure": FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS,
        "no_thanks": FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS,
    },
    FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_START_PROCESS,
        "yes_sure": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE,
        "no_thanks": FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS,
    },
    FeedbackRatingStates.FEEDBACK_RATING_YES_SURE: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "feedback_rating_excellent": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "feedback_rating_poor": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
    },
    FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "very_poor": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "poor": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "fair": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "good": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "excellent": FeedbackRatingStates.FEEDBACK_RATING_YES_SURE_PROCESS,
        "feedback_rating_excellent": FeedbackRatingStates.FEEDBACK_RATING_EXCELLENT,
        "feedback_rating_poor": FeedbackRatingStates.FEEDBACK_RATING_POOR,
    },
    FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS_PROCESS,
        "start_conversation": FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS_PROCESS,
    
    },
    FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS_PROCESS: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_NO_THANKS_PROCESS,
        "start_conversation": FeedbackRatingStates.FEEDBACK_RATING_START_CONVERSATION,
    },
    FeedbackRatingStates.FEEDBACK_RATING_START_CONVERSATION: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_START_CONVERSATION
    },
    FeedbackRatingStates.FEEDBACK_RATING_EXCELLENT: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_EXCELLENT,
    },
    FeedbackRatingStates.FEEDBACK_RATING_POOR: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_POOR_PROCESS,
    },
    FeedbackRatingStates.FEEDBACK_RATING_POOR_PROCESS: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_POOR_PROCESS,
        "valid_response": FeedbackRatingStates.FEEDBACK_RATING_POOR_VALID,
        "invalid_response": FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID
    },
    FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID_PROCESS
    },
    FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID_PROCESS: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID_PROCESS,
        "valid_response": FeedbackRatingStates.FEEDBACK_RATING_POOR_VALID,
        "invalid_response": FeedbackRatingStates.FEEDBACK_RATING_POOR_INVALID
    },
    FeedbackRatingStates.FEEDBACK_RATING_POOR_VALID: {
        "default": FeedbackRatingStates.FEEDBACK_RATING_POOR_VALID
    },
}
