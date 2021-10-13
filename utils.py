import pathlib
from datetime import datetime


Command = str
Name = str
Schedule = str


def add_log_file(command: Command, name: Name) -> str:
    log_file_name = name.replace(" ", "")
    return f"{command} | ts 2>> ~/error_{log_file_name}.err 1>> ~/{log_file_name}.log"


def watch_err_files(name: Name) -> str:
    err = load_logs(name)
    if err == "No log yet":
        return err
    if not err:
        return "Success"
    else:
        return "Failed"


def load_logs(name: Name, typ: str = "err", status: bool = True) -> str:
    log_file_name = name.replace(" ", "")
    home_dir = pathlib.Path().home()
    if typ == "err":
        filename = f"{home_dir}/error_{log_file_name}.err"
    else:
        filename = f"{home_dir}/{log_file_name}.log"
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        return "No log yet"
