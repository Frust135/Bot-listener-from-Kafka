from typing import Dict

from functions.bot import Bot
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
)
from botbuilder.schema import Activity, ConversationReference
from conf import DefaultConfig
from fastapi import Response, Request, APIRouter

router = APIRouter()

CONFIG = DefaultConfig()
SETTINGS = BotFrameworkAdapterSettings(app_id=CONFIG.APP_ID, app_password=CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(settings=SETTINGS)
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()
BOT = Bot(CONVERSATION_REFERENCES)


@router.post("/messages", tags=["bot"])
async def message(req: Request) -> Response:
    """
    The function `messages` processes incoming messages, deserializes the activity, and passes it to the
    bot for processing, returning a response if available.

    """
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(staus=415)
    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return Response(data=response.body, status_code=response.status)
    return Response(status_code=201)


@router.post("/send_message/{message}", tags=["bot"])
async def send_message(message: str):
    """
    Send a message to the user.
    """
    if CONVERSATION_REFERENCES.keys():
        for conversation_reference in CONVERSATION_REFERENCES.values():
            await ADAPTER.continue_conversation(
                conversation_reference,
                lambda turn_context: turn_context.send_activity(message),
                CONFIG.APP_ID,
            )
        return Response(status_code=201)
    return Response(status_code=404)
