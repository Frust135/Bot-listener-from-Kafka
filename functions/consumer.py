import requests
import json
from confluent_kafka import DeserializingConsumer
from conf import DefaultConfig


class ConsumerObject:
    """
    A class representing a Kafka consumer object.

    This class provides methods to deserialize messages and consume messages from a Kafka topic.

    Attributes:
        consumer: The Kafka consumer object.
    """

    def __init__(self):
        self.consumer = DeserializingConsumer(DefaultConfig.KAFKA | {"group.id": "my_group"})
        self.consumer.subscribe(["topic_0"])

    def consume_messages(self):
        """
        Consume messages from the Kafka topic.
        """
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                message_dict = json.loads(msg.value().decode("utf-8"))
                message = message_dict.get("message")
                print(f"Consumed message: {message}")
                self.send_message_to_bot_route(message)
        finally:
            self.consumer.close()

    def send_message_to_bot_route(self, message: str):
        """
        Send a message to the bot_route's send_message endpoint.
        """
        url = f"http://localhost:{DefaultConfig.PORT}/api/bot/send_message/{message}"
        response = requests.post(url)
        return response.status_code
