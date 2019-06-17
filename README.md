# Slack Autoresponder

The Slack autoresponder is a friendly Slack bot, written in python, that reminds you that some folks feel excluded when you refer to a group as "guys".

This bot was the result of the evolution of zatech's original bot, which was inspired by [18F's](https://web.archive.org/web/20170903230255/https://18f.gsa.gov/2016/01/12/hacking-inclusion-by-customizing-a-slack-bot/). Some users had the hypothesis that using the built-in Slack auto responses had the opposite effect from the intention.

## Quickstart

First some configuration:

name | description | optional/required
---- | ----------- | -----------------
SLACKBOT_TOKEN | Slack bot token, I think the simplest way is using a [legacy token](https://api.slack.com/custom-integrations/legacy-tokens). Used for the bot to authenticate with your Slack workspace. | Required
SLACKBOT_REPORT_URL | If you generate a Slack webhook URL and configure it here, then you'll get reports of the form "{'{channel_name}-{user}: count}" to that channel. We use a private channel called `bot-reports` for this to see if the bot is running. | Optional

It's recommended to install the dependencies in a Python virtual environment:

```
python3 -m venv venv
. venv/bin/activate
pip install -U slackclient
```

Then we can go ahead and run the bot with a script like the following:

```bash
export SLACKBOT_TOKEN="<YOUR_TOKEN_HERE>"
export SLACKBOT_REPORT_URL="<YOUR_OPTIONAL_REPORTS_WEBHOOK_URL_HERE>"
python main.py
```
