<h1 align="center"><code>startup.sh</code></h1>

This script sends a Discord push notification when executed. It can be easily scheduled to run at system boot.

## Usage

I placed this script in `/usr/local/bin`, but you can save it anywhere.

```bash
cd /usr/local/bin
```

```bash
sudo nano startup.sh
```

Copy/paste `startup.sh`, make sure to add your Discord webhook URL.

Make executable:

```bash
chmod +x startup.sh
```

To run:

```bash
./startup.sh
```

**or**

```bash
bash startup.sh
```

## Run at Startup

```bash
sudo crontab -e
```

Add the following line:

```
@reboot sleep 30 && /usr/local/bin/startup.sh >/dev/null 2>&1
```

This will execute the script 30 seconds after the system boots.
