#!/usr/bin/env python
import json
import logging
import os
import threading
import time
from collections import defaultdict
from datetime import datetime
from random import choice
from time import sleep

from requests import post
from slackclient import SlackClient


def run_bot():
    token = os.environ.get('SLACKBOT_TOKEN')
    report_url = os.environ.get('SLACKBOT_REPORT_URL')
    slack_client = SlackClient(token)

    global metrics
    metrics = None
    users = {u['id']:  u['name'] for u in slack_client.api_call("users.list")['members']}
    channels = {u['id']:  u['name'] for u in slack_client.api_call('channels.list')['channels']}

    if report_url:
        # Reports are enabled, so start reporting thread
        global last_run
        last_run = None
        metrics = defaultdict(int)

        class ReportingThread(threading.Thread):
            def run(self):
                while True:
                    curr_hour = datetime.utcnow().minute
                    global last_run
                    global metrics
                    if last_run == curr_hour:
                        sleep(5)
                        continue
                    last_run = curr_hour
                    if not metrics:
                        continue
                    try:
                        metrics = json.dumps(metrics)
                        resp = post(
                            url=report_url,
                            json=dict(text=metrics))
                        resp.raise_for_status()
                    except Exception as exc:
                        print(exc)
                    metrics = defaultdict(int)

        reporting = ReportingThread(name='Reporting Thread')
        reporting.start()

    hits = [
        'guyz',
        'hey guys',
        'hi guys',
        'my guys',
        'thanks guys',
        'the guys',
        'these guys',
        'those guys',
        'you guys',
    ]

    base_response = 'Some people in the community find "guys" alienating, next time would you consider _{}_? :slightly_smiling_face: (<http://bit.ly/2uJCn3y|Learn more>)'
    responses = [
        'all',
        'everyone',
        'folks',
        'y\'all',
    ]

    while True:
        if slack_client.rtm_connect():
            print('slack_client RTM connected')
            while True:
                try:
                    events = slack_client.rtm_read()
                except Exception as exc:
                    logging.error('Exception during slack_client.rtm_read', exc, events)
                    break
                for event in events:
                    if event.get('type') != 'message':
                        continue
                    try:
                        if 'text' not in event:
                            continue
                        channel = event['channel']
                        text = event['text']
                        if 'user' not in event:
                            continue
                        user = event['user']
                        if any(hit in text.lower() for hit in hits):
                            response = slack_client.api_call(
                                'chat.postEphemeral',
                                channel=channel,
                                text=base_response.format(choice(responses)),
                                user=user,
                                as_user='true',
                            )
                            if metrics is not None:
                                channel = channels.get(channel)
                                user = users.get(user)
                                if user and channel:
                                    metrics['{}-{}'.format(channel, user)] += 1
                    except Exception as exc:
                        logging.error('Exception while processing message', exc, event)
                time.sleep(1)
        else:
            logging.error('Connection failed, invalid token?')
            break


if __name__ == '__main__':
    run_bot()
