#!/bin/bash

# colours
NO_FORMAT="\033[0m"
F_BOLD="\033[1m"
C_WHITE="\033[38;5;15m"
C_YELLOW="\033[38;5;11m"
C_GREEN4="\033[48;5;28m"

# update
sudo apt update && sudo apt upgrade -y
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[1/8] UPDATE COMPLETE${NO_FORMAT}"

# enable automatic updates
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[2/8] ENABLE AUTOMATIC UPDATES${NO_FORMAT}"

# set hostname
read -p "Enter the hostname: " hostname
sudo hostnamectl set-hostname $hostname
read -p "Enter the time zone: " timezone
sudo timedatectl set-timezone $timezone
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[3/8] SYSTEM LOCALE UPDATED${NO_FORMAT}"

# add a new sudo user
read -p "Enter the username of the new sudo user: " username
sudo adduser $username
sudo usermod -aG sudo $username
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[4/8] NEW USER CREATED${NO_FORMAT}"

# prepare an .ssh folder with an authorized keys file in the new user's home directory
sudo mkdir /home/$username/.ssh
sudo touch /home/$username/.ssh/authorized_keys
read -p "Enter the public key of the new user: " pubkey
echo $pubkey | sudo tee -a /home/$username/.ssh/authorized_keys
sudo chmod 700 /home/$username/.ssh
sudo chmod 600 /home/$username/.ssh/authorized_keys
sudo chown -R $username:$username /home/$username/.ssh
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[5/8] SSH CONFIGURED${NO_FORMAT}"

# disable password authentication and disallow root login
sudo sed -i 's/#Port 22/Port 22/g' /etc/ssh/sshd_config
sudo sed -i 's/#AddressFamily any/AddressFamily inet/g' /etc/ssh/sshd_config
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/g' /etc/ssh/sshd_config
sudo sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
sudo sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/g' /etc/ssh/sshd_config
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[6/8] SSHD LOCKED-DOWN${NO_FORMAT}"

# add a new UFW rule that allows incoming traffic from the IP address currently connected to port 22
current_ip=$(who am i | awk '{print $5}' | tr -d '()')
sudo ufw allow from $current_ip to any port 22
sudo ufw default deny incoming
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[7/8] FIREWALL CONFIGURED${NO_FORMAT}"

# enable ufw and restart sshd
sudo ufw enable
sudo ufw reload
sudo systemctl restart sshd
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}[8/8] SERVICES RESTARTED${NO_FORMAT}"

# send Discord notification
FINISHDATE=$(date +"%d-%b-%Y");
FINISHTIME=$(date +"%T");
RESTARTTIME=$(date +"%T" --date "+10 seconds")
URL="<your-discord-webhook-url>";
JSON_PAYLOAD=$(printf '{"embeds":[{"title":"[%s]","description":"✅ System Configuration Complete %s at %s.\\n**Restarting in 10 seconds! (%s)**","color":65290,"timestamp":""}]}' "$hostname" "$FINISHDATE" "$FINISHTIME" "$RESTARTTIME" | tr -d '\n')
curl -H 'Content-Type: application/json' -X POST -d "$JSON_PAYLOAD" "$URL"
echo -e "${F_BOLD}${C_WHITE}${C_GREEN4}** SENT DISCORD NOTIFICATION **${NO_FORMAT}"

echo ""
echo -e "${F_BOLD}${C_YELLOW}DONE! RESTARTING IN 10 SECONDS!${NO_FORMAT}"
sleep 10

# reboot
sudo reboot
