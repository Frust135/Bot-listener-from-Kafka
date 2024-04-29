import threading
from fastapi import Response, Request, APIRouter
from functions.producer import ProducerObject
from functions.consumer import ConsumerObject

router = APIRouter()


@router.on_event("startup")
async def startup_event():
    """
    Function to handle the startup event.
    It creates a consumer object and starts a separate thread to consume messages.
    """
    consumer = ConsumerObject()
    thread_consumer = threading.Thread(target=consumer.consume_messages)
    if not thread_consumer.is_alive():
        thread_consumer.start()


@router.get("/producer", tags=["kafka"])
async def producer_route() -> Response:
    """
    Handle the producer request.

    Args:
        req (Request): The incoming request object.

    Returns:
        Response: The response object with a status code of 201.
    """
    producer = ProducerObject()
    producer.send_message()
    return Response(status_code=201)
