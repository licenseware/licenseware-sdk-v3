import datetime
import uuid

from licenseware.pubsub.producer import Producer
from licenseware.pubsub.types import EventType, TopicType


def publish_notification(
    producer: Producer,
    tenant_id: str,
    title: str,
    event_type: EventType,
    icon: str = None,
    url: str = None,
    updated_at: str = None,
    fresh_connect: bool = False,
    extra: dict = None,
):

    notification = {
        "id": str(uuid.uuid4()),
        "tenant_id": tenant_id,
        "title": title,
        "event_type": event_type,
        "icon": icon,
        "url": url,
        "read_at": None,
        "updated_at": updated_at or datetime.datetime.utcnow().isoformat(),
        "extra": extra,
    }

    producer.publish(
        topic=TopicType.APP_EVENTS, data=notification, fresh_connect=fresh_connect
    )

    return notification
