# Python Crontab UI
![](static/lcs.png)

This project aims to simplify managing cron jobs. Common issues that we encounter cron are:

- Jobs are failing silently.
- Manually editing `crontab` is error prone.

# Features:

- Adding, Updating, Deleting and running cron jobs is simple.
- It automatically logs the output of your cron jobs.
- Displays when is the next scheduled run.
- Validates if your schedule is a valid cron schedule.
- Displays if your cron job is succesful or if it failed (experimental)

# Quickstart

Start the server by running the following commands.

```bash
https://github.com/benjcabalona1029/python-crontab-ui.git
cd python-crontab-ui-git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app
```
# Notes
- This installs the cron jobs using the current OS user.
- You should use a unique command name. This is used in filtering the cron jobs.
- The log files are installed in your home directory.
    - The filename of the stdout log is `name.log` where `name` is the command name that you choose in the UI, removing all spaces.
    - The filename of the stderr log is `err_name.err`
- To enable the `status` indicator, run the application using the `experimental status` branch. (i.e. before running `uvicorn main:app` run `git checkout experimental_status` or stop the server, then run the previous git command) The current implementation is quite simple, we have a `file_watcher` that checks if there are any contents in the stderr. If there are, it will display the status as failed. Once you're able to debug the issue, delete the stderr file again.

# TODO:

- Improve the UI. I'm not really good at HTML/CSS/JS. I mean, it is useable but it could be better.
- Currently, adding incorrect cron schedule fails silently (in the UI but not in the API) so if you entered an invalid cron schedule, it will simply not add/update the job.
