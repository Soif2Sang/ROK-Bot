import json
import threading
from dataclasses import dataclass, field
from typing import List, Optional
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DiscordWorkerSchema:
    worker: str
    discord_id: str
    channel_id: str

@dataclass_json
@dataclass
class DiscordWorkerListSchema:
    workers: List[DiscordWorkerSchema] = field(default_factory=list)


class DiscordWorkerListSingleton:
    _instance = None
    _lock = threading.Lock()
    _file_path = "discord_worker_list.json"
    worker_list: Optional[DiscordWorkerListSchema] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def write_worker_list(self, worker_list: DiscordWorkerListSchema):
        with self._lock:
            with open(self._file_path, "w") as file:
                json.dump(worker_list.to_dict(), file)
            self.worker_list = worker_list

    def read_worker_list(self) -> DiscordWorkerListSchema:
        with self._lock:
            if self.worker_list is None:
                try:
                    with open(self._file_path, "r") as file:
                        data = json.load(file)
                        self.worker_list = DiscordWorkerListSchema.from_dict(data)
                except FileNotFoundError:
                    self.worker_list = DiscordWorkerListSchema()
                    with open(self._file_path, "w") as file:
                        json.dump(self.worker_list.to_dict(), file)
            return self.worker_list
