#!/usr/bin/env python
import os
import time
from random import choice
from pprint import pprint

from slackclient import SlackClient


def run_bot():
    token = os.environ.get('SLACKBOT_TOKEN')

    slack_client = SlackClient(token)

    hits = [
        "guyz",
        "hey guys",
        "hi guys",
        "my guys",
        "thanks guys",
        "the guys",
        "these guys",
        "those guys",
        "you guys",
    ]

    base_response = 'Some people in the community find "guys" alienating, next time would you consider {}? :slightly_smiling_face: (<http://bit.ly/2uJCn3y|Learn more>)'
    responses = [
        'all',
        'everyone',
        'folks',
        'y\'all',
    ]

    if slack_client.rtm_connect():
        while True:
            events = slack_client.rtm_read()
            for event in events:
                if event.get('type') != 'message':
                    continue
                try:
                    channel = event['channel']
                    text = event['text']
                    user = event['user']
                    if any(hit in text.lower() for hit in hits):
                        response = slack_client.api_call(
                            'chat.postEphemeral',
                            channel=channel,
                            text=base_response.format(choice(responses)),
                            user=user,
                            as_user='true',
                        )
                        print(response)
                except Exception as exc:
                    print("Exception", exc)

            time.sleep(1)
    else:
        print('Connection failed, invalid token?')


if __name__ == '__main__':
    run_bot()
