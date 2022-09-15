import json
from typing import Callable

from licenseware.config.config import Config
from licenseware.utils.logger import log

from .types import EventType, TopicType


class Producer:
    def __init__(
        self,
        producer_factory: Callable,
        config: Config,
        delivery_report: Callable = None,
    ):
        self.config = config
        self.producer_factory = producer_factory
        self.producer = producer_factory(config)
        self.delivery_report = delivery_report
        self._allowed_events = EventType().dict().values()
        self._allowed_topics = TopicType().dict().values()

    def _checks(self, topic, data):

        assert topic in self._allowed_topics
        assert isinstance(data, dict)
        assert data["event_type"] in self._allowed_events

    def publish(self, topic: TopicType, data: dict, delivery_report: Callable = None):

        self._checks(topic, data)
        databytes = json.dumps(data).encode("utf-8")

        # Can't catch any errors from producer... if something goes wrong it will get stuck in producer thread...
        # https://stackoverflow.com/questions/40866634/kafka-producer-how-to-handle-java-net-connectexception-connection-refused

        self.producer.poll(0)
        self.producer.produce(
            topic, databytes, callback=delivery_report or self.delivery_report
        )
        self.producer.flush()

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            log.error("Message delivery failed: {}".format(err))
            raise Exception("Lost connection to kafka...")
        else:
            log.success(
                "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
            )
