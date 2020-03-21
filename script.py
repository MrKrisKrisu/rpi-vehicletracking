############## CONFIG ###############
core_instance="xxx.de"
bssid_area="xx:xx:xx"
scanning_interface="wlan0"
#####################################

from wifi import Cell
import datetime
import time
import requests

found = []
i = 0

while True:
        i += 1
        if i > 240:
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
                                        response = requests.get('https://' + core_instance + '/pi-scan/?bssid=' + cell.address)
                                        print(response.text)
                                else:
                                        print("*** Netzwerk nicht in Lokalisierungsbereich")
                time.sleep(1)
        except Exception as e:
                print(e)
                time.sleep(5)
