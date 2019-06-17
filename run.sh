#!/usr/bin/env bash
set -efu
set -o pipefail

export SLACKBOT_TOKEN="xoxb-XXXXXX-XXXXXXXXXX"
export SLACKBOT_REPORT_URL="https://hooks.slack.com/services/XXXXXX/XXXXXXX/XXXXX"

echo "Starting auto responder..."
python main.py
