import os
import slack
import slack.errors as e


def notify(data):
    print(data)
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    try:
        message_pre = "The following _published_ URLs cannot be accessed. Please examine and unpublish if necessary:\n\n"
        response = client.chat_postMessage(
            channel='#arrival-support-bot-alerts',
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "URL Liveness Probe: Failed Links"
                    }
                },
                {
                    "type": "divider",
                    "block_id": "divider1"
                },
                {
                    "type": "section", "text":
                    {
                        "type": "mrkdwn",
                        "text": message_pre + data,
                    }
                },
            ])
        assert response["ok"]
    except e.SlackApiError as error:
        print(f"Error: {error}")
