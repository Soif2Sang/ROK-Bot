import ast
import os

blacklisted_subdirectories = [
    ".git",
    ".idea",
    "__pycache__",
    "venv",
    "character",
    "Crypto",
    "easyocr",
    "flet_toast",
    "models",
    "twocaptcha",
    "auth compiled",
    "Include",
    "Lib",
    "logs",
    "Scripts",
    "taskscod",
    "tesseract",
    "viewscod",
]


def is_directory_blacklisted(directory):
    return directory in blacklisted_subdirectories


def collect_py_files(root_dir, dic=None):
    if dic is None:
        dic = {}

    for root, subdirs, files in os.walk(root_dir):
        subdirs[:] = [d for d in subdirs if not is_directory_blacklisted(d)]
        for filename in files:
            if filename.endswith(".py"):
                module_name = filename[:-3]  # Remove the .py extension
                directories_and_subdirectories = root.replace("\\", ".")

                for _ in range(2):
                    if directories_and_subdirectories.startswith("."):
                        directories_and_subdirectories = directories_and_subdirectories[1:]

                if not directories_and_subdirectories:
                    dic[module_name] = module_name
                else:
                    dic[module_name] = directories_and_subdirectories + "." + module_name

        for subdir in subdirs:
            subdir_path = os.path.join(root, subdir)
            dic = collect_py_files(subdir_path, dic)

    return dic


result = collect_py_files(".\\", {})

COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"


def check_imports(root_dir, module_name, import_format):
    is_valid = True
    if not os.path.exists(root_dir):
        print(root_dir)
        print(f"{COLOR_RED}Error: File not found for module {module_name}")
        return False

    with open(root_dir, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_module = alias.name
                if imported_module in import_format and not import_format[imported_module] in source_code:
                    print(
                        f"{COLOR_YELLOW}Warning: {module_name}.py imports {imported_module}, but it should import {import_format[imported_module]}"
                    )
                    is_valid = False
        if isinstance(node, ast.ImportFrom):
            imported_module = node.module
            if imported_module in import_format and not import_format[imported_module] in source_code:
                print(
                    f"{COLOR_YELLOW}Warning: {module_name}.py imports {imported_module}, but it should import {import_format[imported_module]}"
                )
                is_valid = False
    return is_valid


verified = True
for module_name, module_path in result.items():
    file_path = os.path.join(".\\", module_path.replace(".", "\\") + ".py")
    import_format = {k: v for k, v in result.items() if k != module_name}
    verified = verified and check_imports(file_path, module_name, import_format)

exit(not verified)
