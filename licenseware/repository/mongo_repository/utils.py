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


def add_update_operators(data: dict, append: bool):

    if not isinstance(data, dict):
        return data

    if not append:
        first_key = list(data.keys())[0]
        if not first_key.startswith("$"):
            data = {"$set": data}
        return data

    set_data = {"$set": {}}
    add_to_set_data = {"$addToSet": {}}
    for k, v in data.items():
        if isinstance(v, (str, int, dict)):
            set_data["$set"].update({k: v})
        if isinstance(v, list):
            add_to_set_data["$addToSet"].update({k: {"$each": v}})

    return {**set_data, **add_to_set_data}
