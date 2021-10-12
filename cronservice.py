from crontab import CronTab
from croniter import croniter
import getpass

_user = getpass.getuser()

_cron = CronTab(user=_user)

Command = str
Name = str
Schedule = str


def _add_log_file(command: Command, name: Name) -> str:
    log_file_name = name.replace(" ", "")
    return f"{command} >> ~/{log_file_name}.log 2>&1"


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
