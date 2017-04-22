# Management Scripts

## Copy/Move the following files
**Destination:** /usr/local/solinst
- modem-comm.sh
- serial_read.py
- web_submit.py
- solinst.ini

**Destination:** /etc/cron.d
- solinst-cron

## Adjust the following
- Create directory: /usr/local/solinst/data
- Make sure /usr/local/solinst/modem-comm.sh has execute permissions (0755)
- Make sure /etc/cron.d/solinst-cron is owned by root
- Edit /usr/local/solinst/solinst.ini
	- Correct serial port (/dev/ttyS0)
	- Correct public and private keys for data.sparkfun.com
