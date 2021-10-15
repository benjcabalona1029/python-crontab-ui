from crontab import CronTab
from croniter import croniter
from datetime import datetime
import getpass

from utils import add_log_file, Command, Name, Schedule, delete_log_file

_user = getpass.getuser()

_cron = CronTab(user=_user)


def add_cron_job(comm: Command, name: Name, sched: Schedule) -> None:
    if croniter.is_valid(sched):
        job = _cron.new(command=add_log_file(comm, name), comment=name)
        job.setall(sched)
        _cron.write()
    else:
        raise ValueError("Invalid Cron Expression")


def update_cron_job(comm: Command, name: Name, sched: Schedule, old_name: Name) -> None:
    match = _cron.find_comment(old_name)
    job = list(match)[0]
    job.setall(sched)
    job.set_command(add_log_file(comm, name))
    job.set_comment(name)
    _cron.write()


def delete_cron_job(name: Name) -> None:
    _cron.remove_all(comment=name)
    _cron.write()
    delete_log_file(name)


def run_manually(name: Name) -> None:
    match = _cron.find_comment(name)
    job = list(match)[0]
    job.run()


def get_next_schedule(name: Name) -> str:
    try:
        match = _cron.find_comment(name)
        job = list(match)[0]
        schedule = job.schedule(date_from=datetime.now())
        return schedule.get_next().strftime("%d/%m/%Y %H:%M:%S").replace("/", "-")
    except IndexError:
        return None
