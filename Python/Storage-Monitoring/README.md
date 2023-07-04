<h1 align="center">💾<br/><code>storage-monitoring.py</code></h1>

## Description
This script monitors the available disk space on different mapped network paths on an Ubuntu 22.04 system, and sends a notification to Discord when the available space falls below a specified threshold.

## Prerequisites
- Ubuntu 22.04
- Python 3.8.10
- pip 20.0.2
- [`requests`](https://pypi.org/project/requests/)
- [`pytz`](https://pypi.org/project/pytz/)
- [`hurry.filesize`](https://pypi.org/project/hurry.filesize/)

## Installation
1. Download `storage-monitoring.py` to `/usr/local/bin`

2. Install the required libraries:
    ```
    pip install requests pytz hurry.filesize
    ```

3. Configure the script:

- Set the `global_notify_threshold_in_bytes` variable to the desired threshold in bytes *(default is 2 GB)*.
- Replace `<Discord_Webhook_URL>` with the actual Discord webhook URL.

4. Run the script
    ```bash
    sudo python3 storage-monitoring.py
    ```

## Usage
The script checks the available disk space on the following network drives, including the local root filesystem:

- NetworkPath1
- NetworkPath2
- NetworkPath3

When the available space on any of these drives falls below the threshold, a Discord notification is sent with the details of the affected drives.

## Example Discord Notification
If any of the drives have less than 2GB disk space remaining, a notification similar to the following will be sent:

```
⚠️ The following drives have less than 2GB disk space remaining!

- **NetworkPath1**
- **NetworkPath2**
- **NetworkPath3**
```

If all drives have sufficient disk space, the notification will indicate that all drives are fine:

```
✅ All drives have sufficient disk space.

- **NetworkPath1**
  (Used <used_space> of <total_space> - **<remaining_space>** remaining)
- **NetworkPath2**
  (Used <used_space> of <total_space> - **<remaining_space>** remaining)
- **NetworkPath3**
  (Used <used_space> of <total_space> - **<remaining_space>** remaining)
```

## Schedule Notifications (Crontab)
1. Enter the crontab:
    ```
    sudo crontab -e
    ```

2. Add the following line:
    ```
    0 6 * * * sudo python3 /usr/local/bin/storage-monitoring.py >/dev/null 2>&1
    ```

This will execute the script each morning at 6:00 AM (system time).

Use [Crontab Generator](https://crontab-generator.org/) or [crontab guru](https://crontab.guru/#) to help generate the cron schedule.
