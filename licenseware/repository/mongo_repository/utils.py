import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from typing import Union


def get_object_id_str(oid: Union[str, ObjectId]):
    
    if isinstance(oid, ObjectId):
        return json.loads(dumps(oid))["$oid"]
    return oid
