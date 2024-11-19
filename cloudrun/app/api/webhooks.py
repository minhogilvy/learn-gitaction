from fastapi import APIRouter, HTTPException, Request, status
from starlette.background import BackgroundTasks
from loguru import logger

from app.schemas.whatsapp.webhooks import WebhookData
from app.services.whatsapp_service import handle_flow
from .version import version
from app.modules.i18n import t
from app.core.settings import (
  MODEL_KEY,
  MODEL_TOKEN
)
from app.types import APIResponse
from app.core.publisher import publisher
from app.core.client import VectorSearchService

from app.config import get_settings
from app.constants import Constants
from ..utils.helpers import Helpers


router = APIRouter()
utils = Helpers()


@router.post("/webhooks/inbound", response_model=APIResponse)
@version(1)
async def inbound_webhook(data: WebhookData, background_tasks: BackgroundTasks, request: Request):
    try:
        # Print request headers
        print("Headers: " + str(request.headers))
    
        print("Body: " + str(data))

        # Get the signature from the header
        signature = request.headers.get('X-Hub-Signature')

        # If no signature is found in the headers, return a 400 error
        if not signature:
            raise HTTPException(status_code=400, detail="Signature missing")

        # Get the raw body of the request to validate the signature
        body = await request.body()

        setttings = get_settings()

        # Verify the signature using the shared secret and request body
        if not utils.verify_signature(setttings.whatsapp_secret_token, body, signature):
            raise HTTPException(status_code=403, detail="Forbidden - Invalid Signature")

        background_tasks.add_task(handle_flow, data, background_tasks)
        return APIResponse(
            code=status.HTTP_200_OK,
            message='SUBMITED_SUCCESS',
            data={}
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/webhooks/inbound")
@version(1)
async def verify_webhook(request: Request) -> int:
    query_params = request.query_params
    mode = query_params.get("hub.mode")
    token = query_params.get("hub.verify_token")
    challenge = query_params.get("hub.challenge")

    # Check the mode and token sent are correct
    if mode == MODEL_KEY and token == MODEL_TOKEN:
        # Respond with 200 OK and challenge token from the request
        return int(challenge)

    # Respond with '403 Forbidden' if verify tokens do not match
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden"
    )

@router.get('/notebook/search')
@version(1)
async def vertex_query() -> None:
  setttings = get_settings()

  print("-- Check event vertex search ai")
  topic_id = setttings.pubsub_generate_annotations_topic
  payload = {
    'event': Constants.QUEUE_PREDICT,
    'images': [
      "https://storage.googleapis.com/vt-gcp-sandbox.appspot.com/testingModule/161494fc-4034-41af-be0e-752c2bfd1d16_frontTeeth.jpg",
      "https://storage.googleapis.com/vt-gcp-sandbox.appspot.com/testingModule/161494fc-4034-41af-be0e-752c2bfd1d16_frontTeeth.jpg",
      "https://storage.googleapis.com/vt-gcp-sandbox.appspot.com/testingModule/161494fc-4034-41af-be0e-752c2bfd1d16_frontTeeth.jpg"
    ]
  }
  response = publisher(payload, topic_id=topic_id)


  