# Python Crontab UI
![](static/lcs.png)

This project aims to simplify managing cron jobs. Common issues that we encounter cron are:

- Jobs are failing silently.
- Manually editing `crontab` is error prone.

# Features:

- Adding, Updating, Deleting and running cron jobs is simple.
- It automatically logs the output of your cron jobs. This can be viewed in the WEB UI.
- Displays when is the next scheduled run.
- Validates if your schedule is a valid cron schedule.
- Displays if your cron job is successful.


**NOTE:** The timestamp for the logs, and the status indicator requires that you use `zsh` instead of `bash`.

## Screenshots

![](readme_images/failed.PNG)

![](readme_images/log.PNG)

# Quickstart

Start the server by running the following commands.

If you are not yet using `zsh`

```bash
sudo apt install zsh -y
# Make sure to accept the prompt to use zsh as your default shell
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# moreutils is needed for a timestamp to be added in the logs
sudo apt install moreutils
```

```bash
git clone https://github.com/benjcabalona1029/python-crontab-ui.git
cd python-crontab-ui
mkdir logs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app
```
# Notes
- This installs the cron jobs using the current OS user.
- You should use a **unique command name**. This is used in filtering the cron jobs.
- The log files are stored in the `logs` directory of this repository.
  - They are automatically deleted, once the job is deleted. I'm not sure if this is a good or bad idea, but it can easily be
updated by updating the `delete_cron_job` function in `cronservice`.
- The implementation for the status indicator is quite simple, we check the last line of the log file for a specific job. If it contain the work
*Failed* then the job will be tagged as failed.

# TODO:

- Improve the UI. I'm not really good at HTML/CSS/JS. I mean, it is usable but it could be better.
