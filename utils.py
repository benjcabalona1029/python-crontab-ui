import pathlib

Command = str
Name = str
Schedule = str


def add_log_file(command: Command, name: Name) -> str:
    log_file_name = name.replace(" ", "")
    return f"{{{command} || echo Failed }} 2>&1 | ts >> logs/{log_file_name}.log"


def delete_log_file(name: Name) -> None:
    try:
        log_file_name = name.replace(" ", "")
        file = pathlib.Path(f"logs/{log_file_name}.log")
        file.unlink()
    except FileNotFoundError:
        return None


def load_logs(name: Name) -> str:
    log_file_name = name.replace(" ", "")
    filename = f"logs/{log_file_name}.log"
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        return "No log yet"


def watch_status(name: Name) -> str:
    log = load_logs(name)
    if log == "No log yet":
        return log
    try:
        resp = log.split()[-1]
        if resp == "Failed":
            return resp
        else:
            return "Success"
    except IndexError:
        return "No log yet"
