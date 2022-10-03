from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import Producer as KafkaProducer

from licenseware import Config, Consumer, EventType, Producer, TopicType
from . import config

# pytest -s -v tests/test_kafka.py


def test_kafka_publish():
    def producer_client_factory(config: Config):
        producer_client = KafkaProducer({"bootstrap.servers": config.KAFKA_BROKER_URL})
        return producer_client

    Producer(producer_client_factory, config)

    data_stream = {
        "event_type": EventType.ACCOUNT_CREATED,
        "tenant_id": None,
        "etc": "data",
    }

    # producer.publish(TopicType.USER_EVENTS, data_stream)


def test_kafka_subscriber():
    def consumer_client_factory(config: Config):
        consumer_client = KafkaConsumer(
            {
                "bootstrap.servers": config.KAFKA_BROKER_URL,
                "group.id": config.APP_ID,
            }
        )
        return consumer_client

    consumer = Consumer(consumer_client_factory, config)

    consumer.subscribe(TopicType.USER_EVENTS)

    def account_created_handler(*args, **kwargs):
        return "some processed data"

    # consumer.dispatch(EventType.ACCOUNT_CREATED, account_created_handler)
    # consumer.listen()
