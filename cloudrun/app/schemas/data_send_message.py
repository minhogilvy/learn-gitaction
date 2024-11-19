from typing import List
from pydantic import BaseModel, HttpUrl


class Reply(BaseModel):
    id: str
    title: str


class Button(BaseModel):
    type: str
    reply: Reply


class Action(BaseModel):
    buttons: List[Button]


class Body(BaseModel):
    text: str


class Interactive(BaseModel):
    type: str
    body: Body
    action: Action


class Messages(BaseModel):
    messages: List[str]


class WelcomePrivacyPolicy(BaseModel):
    messages: List[str]
    interactive: Interactive


class IDisagree(BaseModel):
    interactive: Interactive


class Stop(BaseModel):
    interactive: Interactive


class SectionRow(BaseModel):
    id: str
    title: str


class Section(BaseModel):
    title: str
    rows: List[SectionRow]


class ListAction(BaseModel):
    button: str
    sections: List[Section]


class ListInteractive(BaseModel):
    type: str
    body: Body
    action: ListAction


class Gender(BaseModel):
    interactive: ListInteractive


class Location(BaseModel):
    messages: List[str]
    interactive: ListInteractive


class GuardianAuthorizationOptions(BaseModel):
    interactive: Interactive


class ResImage(BaseModel):
    url: HttpUrl
    mime_type: str
    sha256: str
    file_size: int
    id: str
    messaging_product: str


class InvalidMessages(BaseModel):
    invalid_full_name: str
    invalid_phone_number: str
    invalid_email: str
    invalid_country: str
    invalid_date_of_birth: str
    guardian_authorization_needed: str
    guardian_authorization_reminder: str
    country_request_message: str
    invalid_lower_teeth_message: str
    invalid_upper_teeth_message: str
    invalid_front_teeth_message: str


class Data(BaseModel):
    welcome_privacy_policy: WelcomePrivacyPolicy
    show_policy_privacy: WelcomePrivacyPolicy
    i_disagree: IDisagree
    thank_you: List[str]
    stop: Stop
    gender: Gender
    first_name: Messages
    last_name: Messages
    email: Messages
    location: Location
    phone_number: Messages
    date_of_birth: Messages
    guardian_authorization_options: GuardianAuthorizationOptions
    guardian_authorization_reminder_button: GuardianAuthorizationOptions
    invalid_messages: InvalidMessages
    tutorial: IDisagree
    tutorial_check: IDisagree
    tutorial_check_message: Messages
    tutorial_video_text: Messages
    proceed_prompt: IDisagree
    ready_prompt: IDisagree
    dental_analysis: Messages
    ready_prompt_dental_analysis: WelcomePrivacyPolicy
    ready_prompt_process_dental_analysis: IDisagree
    lower_teeth: Messages
    lower_teeth_the_photo: Messages
    upper_teeth: Messages
    upper_teeth_the_photo: Messages
    front_teeth: Messages
    front_teeth_the_photo: Messages
    thank_you_analyze: WelcomePrivacyPolicy
    consent_data_image: IDisagree
    thank_you_analyze_reminder_button: WelcomePrivacyPolicy


class DataQuestions(BaseModel):
    frequency_of_pain_in_teeth_or_gums: Gender
    frequency_of_bleeding_gums: Gender
    loose_or_moving_teeth: Gender
    frequency_of_brushing_teeth: Gender
    frequency_of_sugar_consumption: Gender
    smoking_habits: Gender
    dentist_visits: Gender


class DataReports(BaseModel):
    reports_messages: Messages
    reports_messages_please_wait: Messages
    reports_invalid_input_messages: Messages
    reports_invalid_input_messages_again: Messages
    reports_pdf_url: Messages
    reports_generation_pdf: WelcomePrivacyPolicy
    help_start: IDisagree
    help_make_new_assessment: IDisagree
    help_more_about_oral_care: WelcomePrivacyPolicy
    help_create_report_again: IDisagree
    help_keep_my_data: Messages
    feedback_rating_start: IDisagree
    feedback_rating_yes_sure: Gender
    feedback_rating_no_thanks: IDisagree
    feedback_rating_excellent: Messages
    feedback_rating_poor: Messages
    feedback_rating_poor_invalid: Messages
    feedback_rating_poor_valid: Messages
