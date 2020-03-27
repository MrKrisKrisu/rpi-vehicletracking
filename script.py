############## CONFIG ###############
core_instance="xxx.de"
bssid_area="xx:xx:xx"
scanning_interface="wlan0"
#####################################

from wifi import Cell
import datetime
import time
import requests
import os
import sys

found = []
i = 0
token = " "

def init():
	if os.path.isfile('/opt/rpi-vehicletracking/device_key'):
		f = open('device_key', 'r')
		token = f.readline()
		f.close()
		return token
	else:
		f = open('/opt/rpi-vehicletracking/device_key', "w+")
		reqToken = requests.post('https://' + core_instance + '/api/scan/device/registernew').text
		token = reqToken
		f.write(token)
		f.close()
		return token

token = init()

while True:
        i += 1
        if (i > 60 * 20):
                found = []
                i = 0
        try:
                print(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ": Scan...")
                cells = Cell.all(scanning_interface)
                for cell in cells:
                        if cell.address not in found:
                                print(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ": " + cell.address + " " + cell.ssid)
                                found.append(cell.address)
                                if bssid_area in cell.address:
                                        response = requests.post('https://' + core_instance + '/api/scan', data = {
                                                'bssid': cell.address,
                                                'ssid': cell.ssid,
                                                'signal': cell.signal,
                                                'quality': cell.quality,
                                                'frequency': cell.frequency,
                                                'bitrates': cell.bitrates,
                                                'encrypted': cell.encrypted,
                                                'channel': cell.channel
                                        }, headers={'X-Api-Token': token})
                                        print(response.text)
                                else:
                                        print("*** Netzwerk nicht in Lokalisierungsbereich")
                time.sleep(1)
        except Exception as e:
                print(e)
                time.sleep(5)
