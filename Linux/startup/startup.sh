#!/bin/bash

HOSTNAME=$(hostname)
CURRDATE=$(date +"%d-%b-%Y");
CURRTIME=$(date +"%T");

echo "SYSTEM STARTED "$CURRDATE" AT "$CURRTIME;
echo "";

URL="<discord-webhook-url>";
JSON_PAYLOAD=$(printf '{"embeds":[{"title":"[%s]","description":"🥾 System Booted %s at %s.","color":65290,"timestamp":""}]}' "$HOSTNAME" "$CURRDATE" "$CURRTIME" | tr -d '\n')
curl -H 'Content-Type: application/json' -X POST -d "$JSON_PAYLOAD" "$URL"

exit 1;
