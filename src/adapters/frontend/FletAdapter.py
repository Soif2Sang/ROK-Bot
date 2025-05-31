from src.adapters.frontend.FrontEndAdapter import FrontEndAdapter
from singletons import ss, EmulatorSingleton
self.contextManager

class FletAdapter(FrontEndAdapter):
    def __init__(self, device_id, **kwargs):
        self.device_id = device_id

        emulator = EmulatorSingleton().getEmulatorType()

        for workerId, worker in ss.worker_settings.worker_type[emulator].workers.items():
            for instance in worker.instances:
                if instance.instance == self.device_id:
                    self.worker_id = workerId

    def set_status(self, text: str):
        ss.page.tile_manager.tiles[self.worker_id].set_status(text)

        self.status = text
        self.log(f"Status set to {text}")

    def get_status(self) -> str:
        return self.status

    def log(self, text: str, color=None):
        print(f"FletAdapter: {text}")
        pass