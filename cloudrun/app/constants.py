class Constants:
    MESSAGES_API_URL = 'https://messages-sandbox.nexmo.com/v1/messages'
    MESSAGES_WHATSAPP_API_URL = 'https://graph.facebook.com/v19.0/414720345058060/messages'
    MEDIA_WHATSAPP_API_URL = 'https://graph.facebook.com/v19.0/'
    API_TOKEN = 'EAAYqQMHCwfMBO1X7ZBw6BxCj8syCZCEbSkwmkPD91PrCQAr28xIAWPrh0gTtJEsunH98o21A9MtelUpW1gOQYlfemaZCx3ZAYXhof6UZAOoCdRhtg09UbJrJ89pMyeZA4u5FqyaqtZC8uZAZAwMOLNHDHfenEAxeprzfAWi9a1EUWhjZBdDFCFotL7h9EbFF9uYpLQmQZDZD'
    WHATSAPP_ID = '374507932421575'
    WHATSAPP_NUMBER = "+15556013253"
    COLLECTION_NAME = "usersWhatsApp"
    COLLECTION_AUDIT_TRAIL_LOG = "auditTrailLog"
    COLLECTION_TRAINING_DATA = "trainingData"
    MODEL_TEACHABLE_MACHINE = './model/keras_model.h5'
    LABELS_TEACHABLE_MACHINE = './model/labels.txt'
    BUCKET_NAME = "usersWhatsApp"
    BUCKET_NAME_MODEL = "userPhotos"
    PRIVATE_BUCKET = "prod-colpal-private"
    
    TUTORIAL_VIDEO_URL = "template/tutorial_video.mp4"
    
    LOWER_TEETH_IMAGE_MIRROR_URL = "template/lower_teeth_image_mirror.png"
    LOWER_TEETH_IMAGE_URL = "template/lower_teeth_image.jpg"
    
    UPPER_TEETH_IMAGE_MIRROR_URL = "template/upper_teeth_image_mirror_url.png"
    UPPER_TEETH_IMAGE_URL = "template/upper_teeth_image.jpg"

    FRONT_TEETH_IMAGE_MIRROR_URL = "template/front_teeth_image_mirror_url.png"
    FRONT_TEETH_IMAGE_URL = "template/front_teeth_image.jpg"
  
    HISTORY_BOT = "Bot"

    KEY_LOWER_JAW = "lower jaw"
    KEY_UPPER_JAW = "upper jaw"
    KEY_FRONT_TEETH = "front teeth"
    
    BUCKET_NAME_LOWER_JAW_IMAGE = "lower_jaw"
    BUCKET_NAME_UPPER_JAW_IMAGE = "upper_jaw"
    BUCKET_NAME_FRONT_TEETH_IMAGE = "front_teeth"
    REPORTS_INPUT_TYPE = "1"

    QUEUE_FIREBASE_STATE = "update_firebase_state"
    QUEUE_GENERATE_REPORT = "generate_report"
    QUEUE_VALIDATE_IMAGE = "validate_image"
    QUEUE_PREDICT = "image_predict"
    QUEUE_UPLOAD_IMAGE = "upload_image"
    QUEUE_UPDATE_DATA_CONSENT_TRAIN = "update_data_consent_train"
    QUEUE_DELETE_USER_INFORMATION = "delete_user_information"
    QUEUE_THREAD_PROCESS = "thread_process"
    FAKE_DUMMY = {'calculus': 1, 'caries': 1, 'discoloration': 2, 'gingivitis': 1, 'mouthUlcer': 0}

    ACTION_TYPE_CONSENT = "consent"
    ACTION_TYPE_DE_CONSENT = "de-consent"
    CONSENT_FLOW = "consent_start"
