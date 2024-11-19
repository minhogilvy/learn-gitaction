import json
from app.schemas.data_send_message import Data, ResImage, DataQuestions, DataReports
import requests
from typing import Union


class DataLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance
    
    def _load_data(self):
        json_data = """
{
  "welcome_privacy_policy": {
    "messages": [
      "*Hi there*! Welcome to Colgate's Oral Health Assistant.",
      "To better assist you, could you *please grant permission to receive our messages and allow access to your data*, which will personalize your experience?"
    ],
    "interactive": {
      "type": "button",
      "body": {
        "text": "*By clicking, I agree to receive communications from Colgate, including my personalized oral report, offers, oral care tips and news. All information is managed in accordance with our Privacy Policy.*"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "i_agree",
              "title": "I Agree"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "i_disagree",
              "title": "I Disagree"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "show_terms_policy",
              "title": "Show Privacy Policy"
            }
          }
        ]
      }
    }
  },
  "show_policy_privacy":{
    "messages":["Privacy Policy"],
    "interactive": {
      "type": "button",
      "body": {
        "text": "Are you in agreement with the Privacy Policy and do you wish to proceed?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "show_policy_privacy_i_agree",
              "title": "I agree"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "show_policy_privacy_i_disagree",
              "title": "I disagree"
            }
          }
        ]
      }
    }
  },
  "i_disagree": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Sorry, but without your authorization, we cannot proceed."
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "i_stop_here",
              "title": "Okay, I'll stop here"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "i_accept",
              "title": "I accept the terms"
            }
          }
        ]
      }
    }
  },
  "thank_you": [
    "*Thank you!*",
    "Well, to begin and provide you with a *personalized report*, please fill out the following details.",
    "And don't worry: *Your information will be securely stored for the purpose of delivering your report* and will not be used for any other purposes without your consent.",
    "Let's start with your personal information."
  ],
  "stop": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Okay! We at Colgate-Palmolive appreciate your interest! Thank you for engaging with us!"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "i_reset",
              "title": "Restart conversation"
            }
          }
        ]
      }
    }
  },
  "gender": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "Please, select your gender:"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {
                "id": "male",
                "title": "Male"
              },
              {
                "id": "female",
                "title": "Female"
              },
              {
                "id": "prefer_not_to_say",
                "title": "Prefer not to say"
              },
              {
                "id": "other",
                "title": "Other"
              }
            ]
          }
        ]
      }
    }
  },
  "first_name": {
    "messages": [
      "*[Question 2 of 7]* What's your *first name?*"
    ]
  },
  "last_name": {
    "messages": [
      "*[Question 3 of 7]* What's your *last name?*"
    ]
  },
  "email": {
    "messages": [
      "*[Question 4 of 7]* Now, your email (Please, fill in the following format: abc@email.com):"
    ]
  },
  "location": {
    "messages": [
      "*[Question 5 of 7]* Where are you located? (State – South Africa):"
    ],
    "interactive": {
      "type": "list",
      "body": {
        "text": "Select your location:"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {
                "id": "mpumalanga",
                "title": "Mpumalanga"
              },
              {
                "id": "limpopo",
                "title": "Limpopo"
              },
              {
                "id": "kwazulu_natal",
                "title": "KwaZulu-Natal"
              },
              {
                "id": "gauteng",
                "title": "Gauteng"
              },
              {
                "id": "eastern_cape",
                "title": "Eastern Cape"
              },
              {
                "id": "free_state",
                "title": "Free State"
              },
              {
                "id": "north_west",
                "title": "North West"
              },
              {
                "id": "northern_cape",
                "title": "Northern Cape"
              },
              {
                "id": "western_cape",
                "title": "Western Cape"
              },
              {
                "id": "i_not_in_south_africa",
                "title": "I am not in South Africa"
              }
            ]
          }
        ]
      }
    }
  },
  "phone_number": {
    "messages": [
      "*[Question 6 of 7]* Could you write down your phone number?"
    ]
  },
  "date_of_birth": {
    "messages": [
      "*[Question 7 of 7]* And finally, I'll need your date of birth (Please, fill in the following format: MM/DD/YYYY)"
    ]
  },
  "guardian_authorization_options": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "We're really glad to know you're interested in learning about your health early on. But to proceed, it's important that your guardian authorizes your participation in this experience, okay?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "guardian_authorizes",
              "title": "Guardian authorizes"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "guardian_not_authorized",
              "title": "Guardian not yet"
            }
          }
        ]
      }
    }
  },
  "guardian_authorization_reminder_button": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "To proceed, talk to your guardian. I promise I'll keep waiting here."
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "guardian_authorizes",
              "title": "Guardian authorizes"
            }
          }
        ]
      }
    }
  },
  "invalid_messages": {
    "invalid_full_name": "Sorry! Could you write your name again?",
    "invalid_phone_number": "Sorry, I couldn't recognize this phone number. Could you try again?",
    "invalid_email": "Sorry, I couldn't recognize this email. Can you try again?",
    "invalid_country": "Hmm, I don't think I understood the country you wrote. Could you try rewriting it?",
    "invalid_date_of_birth": "Hmm, are you sure your date of birth is correct? Could you try again?",
    "guardian_authorization_needed": "We're really glad to know you're interested in learning about your health early on. But to proceed, it's important that your guardian authorizes your participation in this experience, okay?",
    "guardian_authorization_reminder": "To proceed, talk to your guardian. I promise I'll keep waiting here.",
    "country_request_message": "Please, tell the country you are located in.",
    "invalid_lower_teeth_message": "Hmm, I couldn't recognize that photo. Could you try again?",
    "invalid_upper_teeth_message": "I think I need another photo, because I can't identify the one you sent. Could you retake it, please?",
    "invalid_front_teeth_message": "I don't think I can use this photo. Could you send me another one, please?"
  },
  "tutorial": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Thank you for providing your details. Now, I need you to take 3 photos of your teeth. To assist you, we have a *video tutorial available.* Would you like to watch it? \\n \\n Remember, *it's not mandatory to watch the tutorial*, and if you don't want to watch it now, you can come back here anytime later."
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "watch_the_tutorial",
              "title": "Watch the tutorial"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "no_thanks",
              "title": "No, thanks"
            }
          }
        ]
      }
    }
  },
  "tutorial_check": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "To watch the video, it's important that you have a good internet connection and space on your phone to download it.\\n\\n Were you able to view it?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "yes_all_good",
              "title": "Yes, all good!"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "no_i_wasnt_able_to",
              "title": "No, I wasn't able to"
            }
          }
        ]
      }
    }
  },
  "tutorial_check_message": {
    "messages": [
      "I will guide you through the tips and photos then, no worries!"
    ]
  },
  "tutorial_video_text": {
    "messages": [
      "Sure! Here it is:"
    ]
  },
  "proceed_prompt": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Can we proceed?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "sure",
              "title": "Sure!"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "not_yet",
              "title": "Not yet"
            }
          }
        ]
      }
    }
  },
  "ready_prompt": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Ok! Whenever you're ready, just continue from where we left off."
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "im_ready",
              "title": "I’m ready!"
            }
          }
        ]
      }
    }
  },
  "dental_analysis": {
    "messages": [
      "So, here are some tips for the best results of your photos:\\n\\n 1. Ensure your teeth are clean.\\n 2. Use natural light.\\n 3. Clean your camera lens.\\n 4. Take the photo at a right angle to your mouth so all teeth and gums are visible.\\n 5. If you're struggling, ask someone to take the photos for you."
    ]
  },
  "ready_prompt_dental_analysis": {
    "messages": [
      "Only submit pictures of your teeth as directed. Any other pictures will be refused and deleted."
    ],
    "interactive": {
      "type": "button",
      "body": {
        "text": "Are you ready?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "yes_ready",
              "title": "Yes, ready!"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "no_wait",
              "title": "No, please wait"
            }
          }
        ]
      }
    }
  },
  "ready_prompt_process_dental_analysis": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Ok! Whenever you're ready, just continue from where we left off."
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "yes_ready",
              "title": "Yes, ready!"
            }
          }
        ]
      }
    }
  },
  "lower_teeth": {
    "messages": [
      "So, here we go. First, send the picture of your *lower teeth.*",
      "*Tip for taking a photo of the lower teeth*: You may need to take the photo from a high angle and/or tilt your head down.\\n\\nYou can also use a mirror to help you. See an example."
    ]
  },
  "lower_teeth_the_photo": {
    "messages": [
      "The photo should look like this:"
    ]
  },
  "upper_teeth": {
    "messages": [
      "Now, please send the picture of your *upper teeth.*",
      "*Tip for taking a photo of the upper teeth:* You may need to take the photo from a low angle and/or tilt your head up.\\n\\nRemember: if you prefer, use the mirror to help you."
    ]
  },
  "upper_teeth_the_photo": {
    "messages": [
      "This is the ideal photo:"
    ]
  },
  "front_teeth": {
    "messages": [
      "Ok! Now, send the picture of your *front teeth.*",
      "*Tip for taking a photo of the front teeth:* You can use your index and middle fingers to retract your lip to show more of your gums.\\n\\nRemember: if you prefer, use the mirror to help you."
    ]
  },
  "front_teeth_the_photo": {
    "messages": [
      "Please ensure the photo matches this example:"
    ]
  },
  "thank_you_analyze": {
    "messages":["Thank you for the photos. I will now analyze them."],
    "interactive": {
      "type": "button",
      "body": {
        "text": "To analyze your oral care condition, I will ask you *a few quick questions.* Is that okay?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "sure",
              "title": "Sure!"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "not_now",
              "title": "Not now"
            }
          }
        ]
      }
    }
  },
  "thank_you_analyze_reminder_button": {
    "messages":["Good! So, let’s do it!"],
    "interactive": {
      "type": "button",
      "body": {
        "text": "Okay! Whenever you're ready, just pick up where we left off."
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "let_continue",
              "title": "Let’s continue"
            }
          }
        ]
      }
    }
  },
  "consent_data_image": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "We would like to use your images for AI model training."
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "consent_image",
              "title": "I give my consent"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "de_consent_image",
              "title": "I revoke my consent."
            }
          }
        ]
      }
    }
  }
}
"""
        json_data_questions = """
{
"frequency_of_pain_in_teeth_or_gums": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "[Question 1 of 6] How often do you feel pain in your teeth or gums?"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {"id": "pain_never", "title": "Never"},
              {"id": "pain_rarely", "title": "Rarely"},
              {"id": "pain_often", "title": "Often"},
              {"id": "pain_always", "title": "Always"}
            ]
          }
        ]
      }
    }
  },
  "frequency_of_bleeding_gums": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "[Question 2 of 6] How often do you notice bleeding gums?"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {"id": "bleeding_never", "title": "Never"},
              {"id": "only_when_brushing", "title": "Only when brushing"},
              {"id": "bleeding_often", "title": "Often, regardless"},
              {"id": "bleeding_always", "title": "Always"}
            ]
          }
        ]
      }
    }
  },
  "loose_or_moving_teeth": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "[Question 3 of 6] Do you feel any teeth are loose or moving?"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {"id": "moving_no", "title": "No"},
              {"id": "moving_one_tooth", "title": "Only one tooth"},
              {"id": "moving_multiple_teeth", "title": "Multiple teeth"}
            ]
          }
        ]
      }
    }
  },
  "frequency_of_brushing_teeth": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "[Question 4 of 6] How often do you brush your teeth?"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {"id": "less_than_once_a_day", "title": "Less than once a day"},
              {"id": "once_a_day", "title": "Once a day"},
              {"id": "twice_a_day", "title": "Twice a day"},
              {"id": "more_than_twice_a_day", "title": "More than twice a day"}
            ]
          }
        ]
      }
    }
  },
  "frequency_of_sugar_consumption": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "[Question 5 of 6] Do you consume sugar frequently? (candy, soft drinks, etc.)"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {"id": "frequently_never", "title": "Never"},
              {"id": "frequently_occasionally", "title": "Occasionally"},
              {"id": "frequently_often", "title": "Often"},
              {"id": "frequently_always", "title": "Always"}
            ]
          }
        ]
      }
    }
  },
  "smoking_habits": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "[Question 6 of 6] Do you smoke?"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {"id": "smoke_no", "title": "No"},
              {"id": "yes_occasionally", "title": "Yes, occasionally"},
              {"id": "yes_daily", "title": "Yes, daily"}
            ]
          }
        ]
      }
    }
  },
  "dentist_visits": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "Going to dentist?"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {"id": "dentist_always", "title": "Always"},
              {"id": "dentist_often", "title": "Often"},
              {"id": "dentist_rarely", "title": "Rarely"},
              {"id": "dentist_never", "title": "Never"}
            ]
          }
        ]
      }
    }
  }
}
"""
        json_data_reports = """
     {
  "reports_messages": {
    "messages": [
      "Right! Thanks for your time and answers. Based on the images provided and your information, I can identify *potential oral health scenarios.*\\n\\n Please note: *this assessment is not a diagnosis* but an evaluation indicating your risk for possible conditions.",
      "Here are the possible conditions I've identified:",
      "Text with the conditions that the bot identified.",
      "Would you like to receive a *personalized assessment report* about your oral health?\\n\\n If you agree, *type 1* to receive it."
    ]
  },
  "reports_messages_please_wait": {
    "messages": [
     " Please wait..."
    ]
  },
  "reports_invalid_input_messages": {
    "messages": [
      "Hmm, sorry. I don't think I understood. If you would like to receive a customized report, please type 1."
    ]
  },
  "reports_invalid_input_messages_again": {
    "messages": [
      "I still don't think I understand. Could you try again, please?"
    ]
  },
  "reports_pdf_url": {
    "messages": [
      "Sure! Here is your personalized oral care report."
    ]
  },
  "reports_generation_pdf": {
    "messages": [
      "Remember, for accurate assessment and treatment, always consult a dental professional",
      "Additionally, for personalized oral care tips and updates, *you're now subscribed to receive messages from Colgate!* Feel free to reach out anytime."
    ],
    "interactive": {
      "type": "button",
      "body": {
        "text": "Can I help with anything else?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "no_help",
              "title": "No, that's all :)"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "need_help",
              "title": "I still need help"
            }
          }
        ]
      }
    }
  },
  "help_start": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "What would you like to do?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "make_new_assessment",
              "title": "Make new assessment"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "more_about_oral_care",
              "title": "More about oral care"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "nothing_thats_all",
              "title": "Nothing! That’s all"
            }
          }
        ]
      }
    }
  },
  "help_make_new_assessment": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Ok! Would you like to create another one for *yourself* or for *someone else*?\\n\\nIf you choose to create it for someone else, the data saved will be from the last person who made the report.\\n\\nIf you want to keep your data saved, we recommend sharing this chat experience, so they can make the evaluation on another mobile device.\\n\\nWhat do you want to do?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "keep_my_data",
              "title": "Keep my data"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "create_report_again",
              "title": "Create report again"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "for_someone_else",
              "title": "For someone else"
            }
          }
        ]
      }
    }
  },
  "help_create_report_again": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Alright! For that, I'll need you to send the 3 photos again and answer the questionnaire once more, okay?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "help_yes_do_it",
              "title": "Yes, let's do it"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "help_no",
              "title": "No"
            }
          }
        ]
      }
    }
  },
  "help_more_about_oral_care": {
    "messages": [
      "Perfect! See all the latest news about oral health.",
      "Send news about Colgate and the latest brand campaigns."
    ],
    "interactive": {
      "type": "button",
      "body": {
        "text": "I hope you liked it! Can I help you with anything else?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "make_new_assessment",
              "title": "Make new assessment"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "no_for_now",
              "title": "Not for now"
            }
          }
        ]
      }
    }
  },
  "help_keep_my_data": {
    "messages": [
      "If you know someone who wants to learn about oral dental conditions, please *share this link* so they can talk to me.",
      "Send the WhatsApp link for the person to share with another person."
    ]
  },
  "feedback_rating_start": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Thank you for using *Colgate's Oral Health Assistant* to assess your oral care conditions.\\n\\nWe hope we were able to provide helpful insights. Your feedback is valuable to us!\\n\\nCould you please take a moment to rate your experience?"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "yes_sure",
              "title": "Yes, sure!"
            }
          },
          {
            "type": "reply",
            "reply": {
              "id": "no_thanks",
              "title": "No, thanks!"
            }
          }
        ]
      }
    }
  },
  "feedback_rating_yes_sure": {
    "interactive": {
      "type": "list",
      "body": {
        "text": "From 1 to 5, where 1 is very poor and 5 is excellent, how would you rate the experience you had in this conversation?"
      },
      "action": {
        "button": "Options",
        "sections": [
          {
            "title": "SELECTION",
            "rows": [
              {
                "id": "very_poor",
                "title": "1 (Very poor)"
              },
              {
                "id": "poor",
                "title": "2 (Poor)"
              },
              {
                "id": "fair",
                "title": "3 (Fair)"
              },
              {
                "id": "good",
                "title": "4 (Good)"
              },
              {
                "id": "excellent",
                "title": "5 (Excellent)"
              }
            ]
          }
        ]
      }
    }
  },
  "feedback_rating_no_thanks": {
    "interactive": {
      "type": "button",
      "body": {
        "text": "Thank you again! We appreciate you taking the time to assess your oral care conditions with us.\\n\\nRemember, maintaining good oral hygiene is essential for a healthy smile.\\n\\nIf you have any questions in the future or need further assistance, feel free to reach out. Have a wonderful day!"
      },
      "action": {
        "buttons": [
          {
            "type": "reply",
            "reply": {
              "id": "start_conversation",
              "title": "Start conversation"
            }
          }
        ]
      }
    }
  },
  "feedback_rating_excellent": {
    "messages": [
      "Your feedback motivates us! Thank you very much for your help!"
    ]
  },
  "feedback_rating_poor": {
    "messages": [
      "Sorry the experience wasn't as you'd like. Could you tell us in up to 255 characters what we could improve?"
    ]
  },
  "feedback_rating_poor_invalid": {
    "messages": [
      "Oops! I think there are more than 15 words in your response. Can you make it shorter?"
    ]
  },
  "feedback_rating_poor_valid": {
    "messages": [
      "We appreciate your feedback and promise to consider everything you've told us."
    ]
  }
}
"""
        
        self._data = Data(**json.loads(json_data))
        self._data_questions = DataQuestions(**json.loads(json_data_questions))
        self._data_reports = DataReports(**json.loads(json_data_reports))
    
    def get_data(self):
        return self._data
    
    def get_data_questions(self):
        return self._data_questions
    
    def get_data_reports(self):
        return self._data_reports


def get_data():
    return DataLoader().get_data()


def get_data_questions():
    return DataLoader().get_data_questions()


def parse_res_image(res_image_data: dict) -> Union[ResImage, None]:
    try:
        res_image = ResImage(**res_image_data)
        return res_image
    except Exception as e:
        print(f"Error parsing res_image: {e}")
        return None


def get_data_reports():
    return DataLoader().get_data_reports()
