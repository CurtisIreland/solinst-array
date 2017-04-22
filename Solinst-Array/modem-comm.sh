#!/bin/bash

# Do stuff here

function toggle_modem {
	gpio export 18 out

	gpio -g write 18 0
	sleep 8
	gpio -g write 18 1
}

if [ ! -c /dev/ttyUSB2 ]
then
	toggle_modem
fi

/usr/bin/pon fona

sleep 10
/usr/bin/python /usr/local/solinst/web_submit.py

/usr/bin/poff fona

if [ -c /dev/ttyUSB2 ]
then
	toggle_modem
fi
