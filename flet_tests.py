from datetime import datetime

def colorize_name(name):
    # Define your colorization logic here
    return name  # Replace with actual colorization logic

def toString(obj):
    if isinstance(obj, Image.Image) or isinstance(obj, ndarray):
        return 'Image'
    if isinstance(obj, dict):
        return 'Dict'
    return repr(obj)

def colorize_output(output):
    if output is True:
        return f"\033[1;32m{output}\033[0m"  # Green color for True
    elif output is False:
        return f"\033[1;31m{output}\033[0m"  # Red color for False
    elif output is None:
        return f"\033[1;33m{output}\033[0m"  # Yellow color for None
    else:
        return output  # No color for other values

def custom_log(func):
    def wrapper(self, *args, **kwargs):
        args_str = [toString(arg) for arg in args] if args is not None else []
        kwargs_str = [f"{key}={toString(value)}" for key, value in kwargs.items()] if kwargs is not None else []
        arg_str = ", ".join(args_str + kwargs_str)

        func_output = func(self, *args, **kwargs)

        if func_output is True or func_output is False or func_output is None:
            output_str = colorize_output(func_output)
        elif func_output is not None:
            output_str = ", ".join(list(map(toString, func_output)))
        else:
            output_str = "None"

        timestamp = f"[ \033[1;32m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m ]"
        message = f"[ {colorize_name(self.name)} ] {func.__name__}({arg_str}): {output_str}"

        print(f"{timestamp} {message}")

    return wrapper

# Example usage:


class Test:
    def __init__(self):
        self.name = "Jo"

    @custom_log
    def example_function(self, arg1, arg2):
        return arg1, arg2, True, False, None, "Hello"

a = Test()
a.example_function(718, 214)
