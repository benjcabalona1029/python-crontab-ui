from crontab import CronTab
from croniter import croniter
import getpass
import pathlib
from datetime import datetime


def test_cron():
    now = datetime.now()
    now_string = now.strftime("%d/%m/%Y %H:%M:%S").replace("/", "-")
    _user = getpass.getuser()
    cron = CronTab(user=_user)
    name = "Date Logger"
    match = cron.find_comment(name)
    job = list(match)[0]
    schedule = job.schedule(date_from=datetime.now())
    print(schedule.get_next())


def watch_files():
    p = pathlib.Path().home()
    path = f"{p}/error_faulty.err"
    with open(path) as f:
        data = f.read()
        print(data)


if __name__ == "__main__":
    watch_files()
