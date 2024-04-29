import json
import random

from confluent_kafka import SerializingProducer
from conf import DefaultConfig


class ProducerObject:
    """
    A class representing a Kafka producer object.

    This class provides methods to serialize messages, create dump data,
    and send messages to a Kafka topic.

    Attributes:
        producer: The Kafka producer object.
    """

    def __init__(self):
        self.producer = SerializingProducer(DefaultConfig.KAFKA)

    def serializer(self, message):
        """
        Serializes the given message.

        Args:
            message: The message to be serialized.

        Returns:
            The serialized message as a byte string.
        """
        return json.dumps(message).encode("utf-8")

    def create_dump_data(self):
        """
        Creates dump data for testing purposes.

        Returns:
            A dictionary containing random user ID and a message.
        """
        return {"user_id": random.randint(1, 100), "message": "Example message."}

    def delivery_report(self, error, message):
        """
        Callback function to handle message delivery reports.

        Args:
            error: The error (if any) that occurred during message delivery.
            message: The message that was delivered.
        """
        if error is not None:
            print(f"Message delivery failed: {error}")
        else:
            print(f"Message delivered to {message.topic()} [{message.partition()}]")

    def send_message(self):
        """
        Sends a message to the Kafka topic.
        """
        self.producer.produce(
            topic="topic_0",
            key="key",
            value=self.serializer(self.create_dump_data()),
            on_delivery=self.delivery_report,
        )
