# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

from pymongo import MongoClient


def get_mongodb_connection(config: Config):
    mongo_connection = MongoClient(config.mongo_connection_uri)[config.MONGO_DBNAME]
    mongo_connection.list_collection_names()
    return mongo_connection
