from crontab import CronTab
from croniter import croniter
from datetime import datetime
import getpass
import pathlib

_user = getpass.getuser()

_cron = CronTab(user=_user)

Command = str
Name = str
Schedule = str


def _add_log_file(command: Command, name: Name) -> str:
    log_file_name = name.replace(" ", "")
    return f"{command} 2>> ~/error_{log_file_name}.err 1>> ~/{log_file_name}.log"


def watch_files(name: Name) -> str:
    log_file_name = name.replace(" ", "")
    home_dir = pathlib.Path().home()
    filename = f"{home_dir}/error_{log_file_name}.err"
    try:
        with open(filename) as f:
            err = f.read()
            if not err:
                return "Success"
            else:
                return "Failed"
    except FileNotFoundError:
        return "No err log yet"


def add_cron_job(comm: Command, name: Name, sched: Schedule) -> None:
    if croniter.is_valid(sched):
        job = _cron.new(command=_add_log_file(comm, name), comment=name)
        job.setall(sched)
        _cron.write()
    else:
        raise ValueError("Invalid Cron Expression")


def update_cron_job(comm: Command, name: Name, sched: Schedule, old_name: Name) -> None:
    match = _cron.find_comment(old_name)
    job = list(match)[0]
    job.setall(sched)
    job.set_command(_add_log_file(comm, name))
    job.set_comment(name)
    _cron.write()


def delete_cron_job(name: Name) -> None:
    _cron.remove_all(comment=name)
    _cron.write()


def run_manually(name: Name) -> None:
    match = _cron.find_comment(name)
    job = list(match)[0]
    job.run()
    print(job, "executed")


def get_next_schedule(name: Name) -> str:
    match = _cron.find_comment(name)
    job = list(match)[0]
    schedule = job.schedule(date_from=datetime.now())
    return schedule.get_next().strftime("%d/%m/%Y %H:%M:%S").replace("/", "-")
