import datetime
import shutil
import requests
import pytz
import socket
from hurry.filesize import size
from hurry.filesize import alternative

def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

sysName = socket.gethostname().upper()

total, used, free = shutil.disk_usage("/")
nc_total, nc_used, nc_free = shutil.disk_usage("/home/nic/NetworkPath1")
b1_total, b1_used, b1_free = shutil.disk_usage("/home/nic/NetworkPath2")
b2_total, b2_used, b2_free = shutil.disk_usage("/home/nic/NetworkPath3")

global_notify_threshold_in_bytes = 2147483648  # 2 GB


def Discord(msg):

    # Get the current system time in UTC
    now_utc = datetime.datetime.utcnow()

    # Convert to America/Toronto time zone
    tz = pytz.timezone('America/Toronto')
    now_toronto = now_utc.replace(tzinfo=pytz.utc).astimezone(tz)

    # Format the datetime object in ISO 8601 format
    now = now_toronto.isoformat()

    data = {
        # "content": msg,
        # "username": "custom username"
    }
    data["embeds"] = [
        {
            "title": "💾 {} Storage Monitoring".format(sysName),
            "description": msg,
            "color": 15036416,
            "timestamp": now
        }

    ]

    print("\n[+] Sending Discord message\n---\n{}\n---\n".format(msg))
    result = requests.post(
        "<Discord_Webhook_URL>", json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("[+] Payload delivered successfully, code {}.".format(result.status_code))
    print("[+] Sent!\n")


if __name__ == '__main__':
    now = datetime.datetime.now().strftime('%Y-%m-%d %I:%M%p')

    lowDiskSpace = []
    # Check Root filesystem
    if (free < global_notify_threshold_in_bytes):
        lowDiskSpace.append("/")

    # Check NetworkPath1
    if (nc_free < global_notify_threshold_in_bytes):
        lowDiskSpace.append("NetworkPath1")

    # Check NetworkPath2
    if (b1_free < global_notify_threshold_in_bytes):
        lowDiskSpace.append("NetworkPath2")

    # Check NetworkPath3
    if (b2_free < global_notify_threshold_in_bytes):
        lowDiskSpace.append("NetworkPath3")

    if len(lowDiskSpace) > 0:
        str = ""
        for disk in lowDiskSpace:
            str = "**{} - {}**\n".format(str, disk)
        Discord(
            "⚠️ The following drives have less than 2GB disk space remaining!\n{}".format(str))
    else:
        Discord(f"✅ All drives have sufficient disk space.\n*- **NetworkPath1**\n(Used {humansize(nc_used)} of {humansize((nc_free + nc_used))} - **{humansize(nc_free)}** remaining)*\n*- **NetworkPath2**\n(Used {humansize(b1_used)} of {humansize((b1_free + b1_used))} - **{humansize(b1_free)}** remaining)*\n*- **NetworkPath3**\n(Used {humansize(b2_used)} of {humansize((b2_free + b2_used))} - **{humansize(b2_free)}** remaining)*")
