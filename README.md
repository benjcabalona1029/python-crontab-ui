# python-crontab-ui
<hr>
This project aims to simplify managing cron jobs. Common issues that with cron are:

- Jobs are failing silently.
- Manually editing `crontab` is error prone.

## Features:

- Adding, Updating, Deleting and running cron jobs is simple.
- It automatically logs the output of your cron jobs.
- Displays when is the next scheduled run.
- Validates if your schedule is a valid cron schedule.

## TODO:

- Improve the UI. I'm not really good at HTML/CSS/JS. I mean, it is useable but it could be better.
- Currently, adding incorrect cron schedule fails silently (in the UI but not in the API) so if you entered an invalid cron schedule, it will simply not add/update the job.
