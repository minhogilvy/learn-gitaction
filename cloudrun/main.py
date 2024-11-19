import base64
import json
import functions_framework # type: ignore
from cloudevents.http.event import CloudEvent # type: ignore
from loguru import logger
from typing import Dict, Any
from app.modules.pubsub.queue import QueueProcessor

@functions_framework.cloud_event
def learnActioinEventProcessor(cloud_event: CloudEvent) -> None:
    # Triggered from a message on a Cloud Pub/Sub topic.

    try:
      # Extract and decode the Pub/Sub message data
      pubsub_message = cloud_event.data.get('message', {})
      encoded_data = pubsub_message.get('data')

      if not encoded_data:
          logger.warning("No data found in the Pub/Sub message.")
          return

      decoded_data = base64.b64decode(encoded_data).decode('utf-8')

      # Convert the JSON string to a Python dictionary
      payload: Dict[str, Any] = json.loads(decoded_data)
      processor = QueueProcessor()
      processor.handle(payload)

    except (ValueError, json.JSONDecodeError) as json_error:
        logger.error(f"JSON decoding error: {json_error}")

    except Exception as e:
        logger.error(f"Error processing event: {e}")

@functions_framework.http
def health(event):
  return "OK"
