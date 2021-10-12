from crontab import CronTab
from croniter import croniter
import getpass
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


if __name__ == "__main__":
    test_cron()
