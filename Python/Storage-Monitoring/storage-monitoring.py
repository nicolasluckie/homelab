import datetime
import shutil
import requests
import pytz
import socket

"""
GLOBAL VARIABLES
"""
SYSNAME = socket.gethostname().upper()
TIMEZONE = "America/Toronto"
PATHS = ["/mnt/BACKUP", "/mnt/BACKUP2"]
THRESHOLD_PERCENTAGE = 25
DISCORD_WEBHOOK_URL = "<your_Discord_webhook_URL>"

"""
This function takes an integer, `nbytes`, representing a count of bytes,
and converts it into a string that represents the byte count in a human readable format.
The output string is formatted to two decimal places and uses appropriate units,
(B, KB, MB, GB, TB, PB) based on the size of the byte count.

@param nbytes (int): The number of bytes to be converted.
@return str: A string representing the byte count in a human readable format.
"""
def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

"""
This function takes a string message, formats it into an embed object and
sends it to a Discord channel via webhook.

@param msg (str): The message to be sent to the Discord channel.
"""
def Discord(msg):

    # Get the current system time in UTC
    now_utc = datetime.datetime.utcnow()

    # Convert to America/Toronto time zone
    tz = pytz.timezone(TIMEZONE)
    tz_converted = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)

    # Format the datetime object in ISO 8601 format
    now = tz_converted.isoformat()

    data = {
        # "content": msg,
        # "username": "custom username"
        "embeds": [
            {
                "title": f"💿 {SYSNAME} Storage Monitoring",
                "description": msg,
                "color": 15036416,
                "timestamp": now
            }
        ]
    }

    print(f"\n[+] Sending Discord message\n\n---\n{msg}\n---\n")
    result = requests.post(DISCORD_WEBHOOK_URL, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"[+] Payload delivered successfully, code {result.status_code}.")
    print("[+] Sent!\n")

if __name__ == '__main__':
    # Create a dictionary to store disk usage
    disk_usage = {}

    # Create an array to store disks below set threshold
    low_disk_space = []

    # Get current disk usage for each path and check if it's below the threshold
    for path in PATHS:
        total, used, free = shutil.disk_usage(path)
        disk_usage[path] = {"name": path.split("/")[-1], "total": total, "used": used, "free": free, "THRESHOLD_IN_BYTES" : round}
        free_percent = round(free / total * 100)
        
        if free_percent < THRESHOLD_PERCENTAGE:
            low_disk_space.append(disk_usage[path])
    
    # Send Discord notification based on length of low disks array
    output_str = ""
    if len(low_disk_space) > 0:
        for disk in low_disk_space:
            output_str += f"\n- **{disk['name']}:** Used {humansize(disk['used'])} of {humansize(disk['total'])} - {humansize(disk['free'])} free (~{round((disk['free'] / disk['total']) * 100)}%)"
        Discord(f"### ⚠️ Low Disk Space Warning\nThreshold: {THRESHOLD_PERCENTAGE}%{output_str}")
    else:
        for disk in disk_usage.values():
            output_str += f"\n- **{disk['name']}:** Used {humansize(disk['used'])} of {humansize(disk['total'])} - {humansize(disk['free'])} free (~{round((disk['free'] / disk['total']) * 100)}%)"
        Discord(f"### ✅ All shares have sufficient disk space\nThreshold: {THRESHOLD_PERCENTAGE}%{output_str}")
