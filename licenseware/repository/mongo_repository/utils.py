import json
from typing import Union

from bson.json_util import dumps
from bson.objectid import ObjectId


def get_object_id_str(oid: Union[str, ObjectId]):
    if isinstance(oid, ObjectId):
        return json.loads(dumps(oid))["$oid"]
    return oid


def get_object_id(oid: str):
    if ObjectId().is_valid(oid):
        return ObjectId(oid)
    return oid
