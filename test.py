from crontab import CronTab
import time
from datetime import datetime
from croniter import croniter


def test_cron():
    now = datetime.now()
    now_string = now.strftime("%d/%m/%Y %H:%M:%S").replace("/", "-")
    cron = CronTab(user="bcabalona")
    job = cron.new(command="~/analysis/bin/python3 ~/test.py", comment=now_string)
    job.minute.every(2)
    job_standard_output = job.run()
    cron.write()
    print(f"Job was run {now_string}")


# import sqlite3
# import pandas as pd

# con = sqlite3.connect("jobs.db")
# df = pd.read_sql("SELECT * FROM jobs", con)
# print(df)

if __name__ == "__main__":
    if croniter.is_valid("0 wrong_value 1 * *"):
        print("Okay")
    else:
        print("error")
