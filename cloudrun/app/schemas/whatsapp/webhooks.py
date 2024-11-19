from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class WebhookImage(BaseModel):
    mime_type: str
    sha256: str
    id: str


class WebhookButtonReply(BaseModel):
    id: str
    title: str


class WebhookListReply(BaseModel):
    id: str
    title: str


class WebhookInteractive(BaseModel):
    type: str
    button_reply: Optional[WebhookButtonReply] = None
    list_reply: Optional[WebhookListReply] = None


class WebhookMessageContext(BaseModel):
    from_: str = Field(..., alias='from')
    id: str


class WebhookText(BaseModel):
    body: str


class WebhookMessage(BaseModel):
    from_: str = Field(..., alias='from')
    id: str
    timestamp: str
    type: str
    interactive: Optional[WebhookInteractive] = None
    image: Optional[WebhookImage] = None
    text: Optional[WebhookText] = None
    context: Optional[WebhookMessageContext] = None


class WebhookContactProfile(BaseModel):
    name: str


class WebhookContact(BaseModel):
    profile: WebhookContactProfile
    wa_id: str


class WebhookConversation(BaseModel):
    id: str
    origin: Dict[str, str]


class WebhookPricing(BaseModel):
    billable: bool
    pricing_model: str
    category: str


class WebhookStatus(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str
    conversation: Optional[WebhookConversation] = None
    pricing: Optional[WebhookPricing] = None


class WebhookMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class WebhookValue(BaseModel):
    messaging_product: str
    metadata: WebhookMetadata
    contacts: Optional[List[WebhookContact]] = None
    messages: Optional[List[WebhookMessage]] = None
    statuses: Optional[List[WebhookStatus]] = None


class WebhookChange(BaseModel):
    value: WebhookValue
    field: str


class WebhookEntry(BaseModel):
    id: str
    changes: List[WebhookChange]


class WebhookData(BaseModel):
    object: str
    entry: List[WebhookEntry]
