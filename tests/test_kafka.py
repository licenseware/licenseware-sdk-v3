from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import Producer as KafkaProducer

from licenseware import Consumer, EventType, Producer, TopicType

# pytest -s -v tests/test_kafka.py


def test_kafka_publish():

    producer_client = KafkaProducer({"bootstrap.servers": "PLAINTEXT://localhost:9092"})

    producer = Producer(producer_client)

    data_stream = {
        "event_type": EventType.ACCOUNT_CREATED,
        "tenant_id": None,
        "etc": "data",
    }

    producer.publish(TopicType.USER_EVENTS, data_stream)


def test_kafka_subscriber():

    consumer_client = KafkaConsumer(
        {
            "bootstrap.servers": "PLAINTEXT://localhost:9092",
            "group.id": "subscriber-consumer",
        }
    )

    consumer = Consumer(consumer_client)

    consumer.subscribe(TopicType.USER_EVENTS)

    def account_created_handler(*args, **kwargs):
        return "some processed data"

    consumer.dispatch(EventType.ACCOUNT_CREATED, account_created_handler)

    # consumer.listen()
