import subprocess
from time import sleep, time

from utils.android_debug_bridge import Adb, DeviceNotFoundException
from utils.functions import get_dic_instances_ld

bridge = None


class AdbLd(Adb):
    def __init__(self, number: str, host="127.0.0.1", port=5037):
        super().__init__(number, host, port)
        self.is_ld = True

    def update_port(self, instances=None):
        instances = get_dic_instances_ld()
        super().update_port(instances)

    def connect_to_device(self, host="emulator"):
        super().connect_to_device(host)

    def wait_boot_complete(self, timeout=100, timedelta=1):
        """
        :param timeout: second
        :param timedelta: second
        """
        cmd = "getprop sys.boot_completed"

        end_time = time() + timeout

        while True:
            try:
                result = self.shell(cmd)
            except RuntimeError as e:
                self.print(str(e))
                sleep(3)
                continue
            except DeviceNotFoundException as e:
                self.print(str(e))
                sleep(3)
                continue

            if result.strip() == "1":
                return True

            if time() > end_time:
                raise TimeoutError()
            elif timedelta > 0:
                sleep(timedelta)

    # def get_device(self, host="127.0.0.1", fail=0):
    #     try:
    #         self.port = str(self.data[str(self.number)]["port"])
    #         device = self.client.device(f"{host}:{self.port}")

    #         if device is None:
    #             self.print(f"INFO : Device is None, trying to reconnect..")
    #             sleep(2)

    #             if device is None and fail > 45:
    #                 return
    #             if device is None:
    #                 return self.get_device()

    #         return device

    #     except Exception as e:
    #         traceback.print_exc()
    #         self.print("EXCEPTION : Error in connect to device")

    #         self.update_port()
    #         self.start_server()

    #         self.print(f"Adb restarting..")
    #         sleep(20)
    #         self.print(f"Connecting to the device..")

    #         self.connect_to_device()

    #         sleep(5)
    #         return self.get_device()

    def get_device(self, host="emulator", max_attempts=10, timeout=2):
        self.port = str(self.data[str(self.number)]["port"])

        for attempt in range(max_attempts):
            device = self.client.device(f"{host}-{self.port}")

            if device is not None:
                return device

            self.print(f"Device Not Found")
            sleep(timeout)
            self.update_port()

            path = self.FileSingleton.get_path()
            cmd = f"{path['LD-Console'].replace('ldconsole', 'adb')} -s {host}-{self.port} shell eco i"
            subprocess.run(cmd)

        raise DeviceNotFoundException(f"{host}-{self.port}")

    def stop_server(self):
        path = self.FileSingleton.get_path()
        cmd = f"{path['LD-Console'].replace('ldconsole', 'adb')} kill-server"
        subprocess.run(cmd)

    def start_server(self):
        path = self.FileSingleton.get_path()
        cmd = f"{path['LD-Console'].replace('ldconsole', 'adb')} start-server"
        subprocess.run(cmd)

    def is_game_alive(self):
        string = "dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'"
        a = self.shell(string)
        return "lilithgame" in a or "rok" in a or "lilithgames" in a
