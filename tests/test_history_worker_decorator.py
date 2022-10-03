import os
import uuid
import time
from typing import List
from licenseware import WorkerEvent, HistoryLogger, get_mongodb_connection
from . import config


class ProcessRVToolsEvent(metaclass=HistoryLogger):
    def __init__(self, event: dict) -> None:
        self.event = WorkerEvent(**event)
        self.db_connection = get_mongodb_connection(config)
        self.config = config  # the config from settings

    def get_raw_data_from_file(self, filepath: str):
        time.sleep(0.3)
        print("Getting raw data from file")
        return filepath

    def extract_virtual_devices(self, raw_data: List[dict]):
        time.sleep(0.1)
        print("Extracting virtual devices")
        return ["some raw data"]

    def save_virtual_devices(self, virtual_devices: List[dict]):
        time.sleep(0.5)
        print("Saving virtual devices")
        return ["list of virtual devices"]

    def run_processing_pipeline(self):
        for fp in self.event.filepaths:
            self.filepath = fp
            self.filename = os.path.basename(fp)
            raw_data = self.get_raw_data_from_file(filepath=fp)
            virtual_devices = self.extract_virtual_devices(raw_data)
            self.save_virtual_devices(virtual_devices)


# pytest -s -v tests/test_history_worker_decorator.py


def test_history_worker_decorator():

    event = {
        "tenant_id": str(uuid.uuid4()),
        "authorization": str(uuid.uuid4()),
        "uploader_id": "rv_tools",
        "filepaths": ["./tests/test_files/RVTools.xlsx"],
        "clear_data": False,
        "event_id": str(uuid.uuid4()),
        "app_id": "ifmp-service",
    }

    rv_tools = ProcessRVToolsEvent(event)
    rv_tools.run_processing_pipeline()
