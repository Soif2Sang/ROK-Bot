import subprocess

file_path = r"C:\LDPlayer\LDPlayer9\ldconsole.exe"


def get_dic_instances():
    argument = "list2"
    command = [file_path, argument]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    # Print the captured output
    print("Captured Output:", result.stdout.split("\n"))

    emulators = result.stdout.split("\n")
    emulators.pop()

    liste = {}
    for emulator in emulators:
        emulator = emulator.split(",")
        liste[emulator[0]] = {
            "name": emulator[1],
            "instance": emulator[0],
            "port": 5554 + 2 * int(emulator[0]),
        }

    return liste


def get_current_instances(data: dict):
    argument = "runninglist"
    command = [file_path, argument]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    emulators = result.stdout.split("\n")
    emulators.pop()

    liste = []

    for emulator in emulators:
        for e in data.values():
            if e["name"] == emulator:
                liste.append((e["instance"], e["name"]))
    return liste


def get_all_vms_running():
    return get_current_instances(get_dic_instances())


get_all_vms_running()
