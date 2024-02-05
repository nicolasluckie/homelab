"""
This script sends a Discord notification to the specified channel.
The notification includes the current system time in the specified time zone.

The script uses both the `requests` module to send an HTTP request to the Discord API,
and the `argparse` module to parse command-line arguments from the response.

Parameters are read from the `.env` file at the start of the script and used to configure the notifications and API requests.

The script is intended to be used as a template for creating a Discord notification
script that can be customized and extended to suit your needs.

You will need to create a Webhook for the channel in your Discord server.
You can find instructions for creating a webhook here:
https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

You will also need to create a .env file in the same directory as the script
and add the following environment variables:

    # System name (leave blank to use `os.name`)
    SYSNAME=System-Name

    # use "TZ identifier" from this list of acceptable values:
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    TIMEZONE=Etc/UTC

    # Discord Webhook URL
    DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/yourWebhookUrl

The script can be run from the command line using the following command:

    python notify.py arg1

Replace arg1 with the name of the command you want to run.
"""

import requests
import json
import argparse
import logging
import datetime
import pytz
import os
from dotenv import load_dotenv

"""
Setup Variables
"""

# Load environment variables from .env file
load_dotenv()

# Get environment variables
SYSNAME = os.getenv('SYSNAME')

# If the SYSNAME environment variable is not set, use the os.name value
if not SYSNAME:
    SYSNAME = os.name

TIMEZONE = os.getenv('TIMEZONE')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

"""
Function Definitions
"""


def send_request(url, method='get', data=None):
    """
    Sends an HTTP request to the specified URL using the specified method and data.
    If the request is successful, returns the response object.
    If an error occurs, logs the error and returns None.

    Args:
        url (str): The URL to send the request to
        method (str): The HTTP method to use (get or post)
        data (dict): The data to send with the request
    """
    try:
        if method == 'get':
            response = requests.get(url, json=data)
        else:
            response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(err)
    else:
        logging.info("[+] {} Success!".format(response.status_code))
        return response


def send_discord_notification(message, colour):
    """
    The `send_discord_notification()` function sends a message to the Discord channel
    using the specified system name, message, and color. The notification includes
    the current system time in the specified time zone.

    For the colour argument you can choose from a list of colour codes:
    https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812

    or convert a colour from hex (#FFFFFF) to decimal:
    https://www.rapidtables.com/convert/color/hex-to-decimal.html

    Args:
        sysname (str): The system name
        message (str): The message to be sent to the Discord channel
        colour  (str): The notification colour in decimal format
    """

    # Get the current system time in UTC
    now_utc = datetime.datetime.utcnow()

    # Convert to America/Toronto time zone
    tz = pytz.timezone(TIMEZONE)
    tz_converted = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)

    # Format the datetime object in ISO 8601 format
    now = tz_converted.isoformat()
    data = {
        "embeds": [
            {
                "title": SYSNAME,
                "description": message,
                "color": colour,
                "timestamp": now,
            }
        ]
    }
    response = send_request(DISCORD_WEBHOOK_URL, 'post', data)
    return response


def main():
    """Parses command line arguments and performs actions based on the provided command.

    Uses the argparse module to parse command-line arguments,
    then calls the send_discord_notification() function with
    different messages based on the provided command
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['arg1', 'arg2'])
    args = parser.parse_args()

    if args.command == 'arg1':
        send_discord_notification(

            # first Discord() parameter: message
            '## It worked!\n' +
            '**Markdown** is supported with `inline` code,\n' +
            '- even **lists**\n' +
            '  - and ***sub-levels***\n' +
            '    ```\n' +
            '    with nested code blocks!\n' +
            '    ```',

            # second Discord() parameter: colour
            '65280')

    elif args.command == 'arg2':
        send_discord_notification('Green!', '2197560')


"""
Script Start
"""

if __name__ == "__main__":
    main()
