import pytz
import requests
import datetime

"""
This script allows you to send a message to a Discord channel through a webhook. A webhook is a way to send automated messages to a Discord channel without a bot.

The script defines a function called "Discord" that takes a message as an argument. The message is then included in a JSON object that is sent to the webhook URL.
The JSON object also includes a title, description, color, and timestamp.

The timestamp is generated using the current system time in UTC, which is converted to the America/Toronto time zone. The timestamp is then formatted in ISO 8601 format.

The color property in the JSON object sets the color of the message. In this script, it is set to a specific shade of blue.
I generated it using Discohook, a web generator for creating personalized Discord webhooks.
At the bottom of the generator click the JSON Data Editor button to view the code needed to replace the data and data["embeds"] variables.

The test case at the end of the script calls the Discord function and sends a test message to the Discord channel given a discord_webhook_url

Overall, this script provides a simple way to send automated messages to a Discord channel through a webhook.
The script can be easily customized to send different types of messages to different channels.
"""

def Discord(msg):

    # Get the current system time in UTC
    now_utc = datetime.datetime.utcnow()

    # Convert to America/Toronto time zone
    tz = pytz.timezone('America/Toronto')
    now_toronto = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)

    # Format the datetime object in ISO 8601 format
    now = now_toronto.isoformat()

    data = {
        "content": msg,
        "username": "custom username"
    }
    data["embeds"] = [
        {
            "title": "your title",
            "description": "your description",
            "color": 15036416,
            "timestamp": now
        }

    ]

    print("\n[+] Sending Discord message\n---\n{}\n---\n".format(msg))
    result = requests.post(
        "<your_discord_webhook_url>", json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("[+] Payload delivered successfully, code {}.".format(result.status_code))
    print("[+] Sent!\n")


if __name__ == "__main__":
    Discord("Test")