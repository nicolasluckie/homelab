<h1 align="center">💾<br/><code>storage-monitoring.py</code></h1>

## Description

This Python script monitors the disk usage of specified paths and sends a notification to a Discord channel via webhook if the free space falls below a certain threshold. This script has only been tested on Ubuntu 22.04 LTS, but should work on most Unix-based operating systems.

## Dependencies

Python3, if not already installed:

```bash
apt update -y && apt install python3 -y
```

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## Execution

When run, the script checks each path in `PATHS` for its disk usage. If the free space is below `THRESHOLD_IN_BYTES`, it sends a notification to Discord with details of the disk usage.

## Usage
1. Create a new Python file and paste `storage-monitoring.py`

2. Replace the Global Variables with your own and run the script using:
```bash
sudo python3 storage-monitoring.py
```

3. Run the script
```bash
sudo python3 storage-monitoring.py
```

## Scheduled Execution

You can also schedule the script to run at regular intervals using cron:

```bash
sudo crontab -e
```

Add the following line:

```
0 6 * * * sudo python3 /path/to/storage-monitoring.py >/dev/null 2>&1
```

This will execute the script each morning at 6:00 AM (system time).

Use [Crontab Generator](https://crontab-generator.org/) or [crontab guru](https://crontab.guru/#) to help generate the cron schedule.
