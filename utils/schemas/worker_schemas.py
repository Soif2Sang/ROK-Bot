from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal
import shortuuid

from dataclasses_json import dataclass_json

from utils.schemas.emulator_schemas import MinMaxSchema


@dataclass_json
@dataclass
class InstanceSchema:
    instance: str


@dataclass_json
@dataclass
class WorkerSettingsSchema:
    name: str = ""
    loop_task: bool = True
    close_emulator: bool = True
    waiting_cooldown: MinMaxSchema = field(default_factory=lambda: MinMaxSchema(min=60, max=120))
    instances: List[InstanceSchema] = field(default_factory=list)


@dataclass_json
@dataclass
class WorkerListSchema:
    workers: Dict[str, WorkerSettingsSchema] = field(default_factory=dict)


@dataclass_json
@dataclass
class WorkerTypeSchema:
    workers: Dict[str, WorkerSettingsSchema] = field(default_factory=dict)
    # worker_type: Dict[str, WorkerListSchema] = field(default_factory=dict)
