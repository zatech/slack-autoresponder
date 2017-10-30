from slackclient import SlackClient
from random import randint
from pprint import pprint
import time
import os

token = os.environ.get('SLACKBOT_LUMBERGH_TOKEN')

slack_client = SlackClient(token)


hits = [
"you guys", 
"these guys",
"my guys",
"those guys",
"hey guys",
"hi guys",
"the guys",
"these guys",
"thanks guys",
"guyz"
]

responses = [
'Some people in the community find "guys" alienating, next time would you consider folks? :slightly_smiling_face: (<http://bit.ly/2uJCn3y|Learn more>)',
'Some people in the community find "guys" alienating, next time would you consider all? :slightly_smiling_face: (<http://bit.ly/2uJCn3y|Learn more>)',
'Some people in the community find "guys" alienating, next time would you consider y\'all? :slightly_smiling_face: (<http://bit.ly/2uJCn3y|Learn more>)',
'Some people in the community find "guys" alienating, next time would you consider everyone? :slightly_smiling_face: (<http://bit.ly/2uJCn3y|Learn more>)'
]

if slack_client.rtm_connect():
    while True:
        events = slack_client.rtm_read()
        for event in events:
            if (
                'channel' in event and
                'text' in event and
                'user' in event and
                'ts' in event and
                event.get('type') == 'message'
            ):
                channel = event['channel']
                text = event['text']
                user = event['user']
                for hit in hits:
                    if hit in text.lower():
                        slack_client.api_call(
                            'chat.postEphemeral',
                             channel=channel,
                             text=responses[randint(0, len(responses)-1)],
                             user = user,
                             as_user = 'true',
                            )
                        break
        time.sleep(1)
else:
    print('Connection failed, invalid token?')