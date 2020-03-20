############## CONFIG ###############
core_instance="xxx.de"
bssid_area="xx:xx:xx"
scanning_interface="wlan0"
#####################################

from wifi import Cell, Scheme
import datetime
import time
import requests

found = []

while True:
        try:
                print(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ": Scan...")
                cells = Cell.all(scanning_interface)
                for cell in cells:
                        if cell.address not in found:
                                print(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ": " + cell.address + " " + cell.ssid)
                                found.append(cell.address)
                                if bssid_area in cell.address:
                                        response = requests.get('https://' + core_instance + '/pi-scan/?bssid=' + cell.address)
                                        print(response.text)
                                else:
                                        print("*** Netzwerk nicht in Lokalisierungsbereich")
                time.sleep(1)
        except Exception as e:
                print(e)
                time.sleep(5)
