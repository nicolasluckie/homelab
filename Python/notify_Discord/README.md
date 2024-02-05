# notify.py

This script sends a Discord notification to the specified channel.
The notification includes the current system time in the specified time zone.

The script uses both the `requests` module to send an HTTP request to the Discord API,
and the `argparse` module to parse command-line arguments from the response.

Parameters are read from the `.env` file at the start of the script and used to configure the notifications and API requests.

The script is intended to be used as a template for creating a Discord notification
script that can be customized and extended to suit your needs.

![Animation](Animation.gif)

## Getting Started

### Prerequisites

Ensure the Python extension for Visual Studio Code is installed

You will need to create a Webhook for a channel in your Discord server.
You can find instructions for creating a webhook here:
https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

### Installation

1. Clone this project and open the `notify_Discord` folder in Visual Studio Code

2. Create a Python Virtual Environment

   - (`Ctrl`+`Shift`+`P`) → `Python: Create Environment`

   - Select `Venv`

   - Select your interpreter *(use Python 3 or latest)*

3. Press (`Ctrl`+`Shift`+<code>`</code>) to launch a new terminal

    - By default VS Code starts a new PowerShell terminal

4. Click the **Launch Terminal** drop-down arrow to the right of the plus icon in the terminal window

5. Select **Command Prompt** to open a new Command Prompt terminal

    - You should see `(.venv)` before the path in your terminal. If not, you can manually activate the virtual environment with this command:

        ```
        .venv/Scripts/activate
        ```

6. Install the required dependencies

    ```
    pip install -r requirements.txt
    ```

7. Rename the `.env.sample` file to `.env` in the same directory as the script and add the following environment variables:

    ```ini
    # System name (leave blank to use `os.name`)
    SYSNAME=System-Name

    # use "TZ identifier" from this list of acceptable values:
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    TIMEZONE=Etc/UTC

    # Discord Webhook URL
    DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/yourWebhookUrl
    ```

## Usage

Run using Command Prompt:

```
python notify.py arg1
```

Where `arg1` is the name of the command you want to run

## Setting up Task Scheduler

To automate the execution of the script, you can create a task in the Task Scheduler.

1. Open **Task Scheduler** from the Start Menu

2. Select ***"Create Basic Task..."*** from the toolbar on the right

3. Name the task

4. Choose a trigger

5. Under **"Action"**, choose ***"Start a program"***

    - Program/script: `"C:\path\to\.venv\Scripts\python.exe"`
    - Add arguments: `notify.py arg1 arg2`
    - Start in: `"C:\path\to\notify.py"`

6. Finish the wizard to create the task.

    - `notify.py` will automatically run according to the trigger you set
