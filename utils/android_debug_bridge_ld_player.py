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
        path = self.FileSingleton.get_path()

        while True:
            try:
                cmd = f"{path['LD-Console'].replace('ldconsole', 'adb')} -s emulator-{self.port} shell getprop sys.boot_completed"

                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                print(result.stdout)

            except RuntimeError as e:
                self.print(str(e))
                sleep(0.5)
                continue
            except DeviceNotFoundException as e:
                self.print(str(e))
                sleep(0.5)
                continue

            if result.stdout.strip() == "1":
                return True

            if time() > end_time:
                raise TimeoutError()
            elif timedelta > 0:
                sleep(timedelta)

    def get_device(self, host="emulator", fail=0):
        self.port = str(self.data[str(self.number)]["port"])
        device = self.client.device(f"{host}-{self.port}")

        if device is None and fail < 15:
            self.print(f"fail {fail}")
            return self.get_device(fail=fail + 1)

        elif device is None and fail == 15:
            self.print(f"fail {fail}")
            self.stop_server()
            sleep(1)
            self.start_server()
            sleep(1)
            return self.get_device(fail=fail + 1)

        elif device is None and fail > 15:
            self.print(f"fail {fail}")
            raise DeviceNotFoundException(f"{host}-{self.port}")
        return device

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
