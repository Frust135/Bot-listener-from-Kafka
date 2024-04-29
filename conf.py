from fastapi import FastAPI
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)


class DefaultConfig:
    """Kafka Configuration"""

    PORT = 8443
    HOST = "0.0.0.0"
    APP_ID = os.environ.get("APP_ID")
    APP_PASSWORD = os.environ.get("APP_PASSWORD")
    KAFKA = {
        "bootstrap.servers": "",
        "security.protocol": "",
        "sasl.mechanisms": "",
        "sasl.username": "",
        "sasl.password": "",
    }


config = DefaultConfig()
logger.info("Starting Kafka POD...")
