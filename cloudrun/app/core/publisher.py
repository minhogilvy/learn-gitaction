from ..modules.pubsub import publish
from ..config import get_settings
settings = get_settings()

def publisher(data, **kwargs) -> str:
    topic_ = kwargs.get('topic_id', settings.pubsub_generate_annotations_topic)
    message_id = publish(topic=topic_, data=data, **kwargs)
    return message_id
