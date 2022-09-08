import pytest
import json
from licenseware import Producer, Consumer, TopicType, EventType
from confluent_kafka import Producer as KafkaProducer
from confluent_kafka import Consumer as KafkaConsumer


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

    def account_created_handler(*args, **kwargs):
        return "some processed data"

    consumer.dispatch(EventType.ACCOUNT_CREATED, account_created_handler)

    # consumer.listen()

    try:

        while True:
            msg = consumer.consumer.poll(0.3)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print("Received message: {}".format(msg.value()))

            data = json.loads(msg.value().decode("utf-8"))

            event_type_found = "event_type" in data.keys()
            tenant_id_found = "tenant_id" in data.keys()

            if event_type_found and tenant_id_found:
                print(
                    "Consumer error: `event_type` and `tenant_id` not found on message."
                )
                continue

            consumer.event_dispacher[data["event_type"]](**data)

    except Exception as err:
        print(err)
        consumer.consumer.close()
