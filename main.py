#!/usr/bin/env python
import logging
import os
import time
from random import choice

from slackclient import SlackClient


def run_bot():
    token = os.environ.get('SLACKBOT_TOKEN')

    slack_client = SlackClient(token)

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
                    except Exception as exc:
                        logging.error('Exception while processing message', exc, event)
                time.sleep(1)
        else:
            logging.error('Connection failed, invalid token?')
            break


if __name__ == '__main__':
    run_bot()
