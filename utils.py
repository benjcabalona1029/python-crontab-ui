import pathlib
from datetime import datetime


Command = str
Name = str
Schedule = str


def add_log_file(command: Command, name: Name) -> str:
    log_file_name = name.replace(" ", "")
    return f"{command} 2>> ~/error_{log_file_name}.err 1>> ~/{log_file_name}.log"


def watch_err_files(name: Name) -> str:
    err = load_logs(name)
    if err == "No log yet":
        return err
    if not err:
        return "Success"
    else:
        return "Failed"


def _add_date(file: str) -> str:
    now = datetime.now()
    now_string = now.strftime("%d/%m/%Y %H:%M:%S").replace("/", "-")
    append = [f"{now_string} {line}" for line in file.splitlines()]
    return "\n ".join(append)


def load_logs(name: Name, typ: str = "err", status: bool = True) -> str:
    log_file_name = name.replace(" ", "")
    home_dir = pathlib.Path().home()
    if typ == "err":
        filename = f"{home_dir}/error_{log_file_name}.err"
    else:
        filename = f"{home_dir}/{log_file_name}.log"
    try:
        with open(filename) as f:
            if status:
                return f.read()
            else:
                return _add_date(f.read())
    except FileNotFoundError:
        return "No log yet"
