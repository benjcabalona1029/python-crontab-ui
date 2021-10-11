from crontab import CronTab
from croniter import croniter
import getpass

_user = getpass.getuser()


_cron = CronTab(user=_user)


def set_log_file(command: str, name: str) -> str:
    log_name = name.replace(" ", "")
    return f"{command} >> ~/{log_name}.log 2>&1"


def add_cron_job(comm: str, name: str, sched: str) -> None:
    if croniter.is_valid(sched):
        job = _cron.new(command=set_log_file(comm, name), comment=name)
        job.setall(sched)
        _cron.write()
    else:
        raise ValueError("Invalid Cron Expression")


def update_cron_job(comm: str, name: str, sched: str, old_name: str) -> None:
    match = _cron.find_comment(old_name)
    job = list(match)[0]
    job.setall(sched)
    job.set_command(set_log_file(comm, name))
    job.set_comment(name)
    _cron.write()


def delete_cron_job(name: str) -> None:
    _cron.remove_all(comment=name)
    _cron.write()


def run_manually(name: str) -> None:
    match = _cron.find_comment(name)
    job = list(match)[0]
    job.run()
    print(job, "executed")
