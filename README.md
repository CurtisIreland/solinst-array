# solinst-array
This is a personal project to read data from sensors

See the Design folder for instructions to connect hardware

## Preparing the Raspberry Pi

These instructions are based on a clean, updated install of Raspbian Linux

- Install the following packages
	- exim4-base
	- ppp
	- screen
- Run raspi-config
	- Configure localization
		- keyboard: Generic 104PC, English US
		- Timezone: America/Toronto
	- Enable sshd
	- Enable serial console
- Edit /boot/cmdline.txt
	- remove "console=serial0,115200" from line
- Reboot Raspberry Pi

## Software install

Follow the README.md instructions from the Solinst-Array and pi-comm directories.

**pi-comm** : Files needed to get the GSM modem to create ppp links for data exchange
**Solinst-Array** : Scripts to run and manage the data collection and transmission

## Arduino

Two Arduino programs to test the connections, and the communications program to help the Pi interact with the sensors
- Solinst-Array : Software to help the Raspberry Pi interact with the connected instruments
- Solinst-TestData : Send fake, formatted data to test communications from the Raspberry Pi
- RainCounter : Test the operation and data readings from the rain collection instrument.

## Communicating with Sparkfun Data collection

http://data.sparkfun.com/input/[publicKey]?private_key=[privateKey]&collect_date=[value]&dht_humid=[value]&dht_temp=[value]&rain_rate=[value]&soil_humid=[value]&soil_temp=[value]&sol_depth=[value]&sol_temp=[value]
