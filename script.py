#!/usr/bin/python3 -u

import datetime
import queue
import threading
import time
import configparser
import requests
from wifi import Cell

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

############## CONFIG ###############
verbose = config['SCRIPT']['verbose']
core_instance = config['SERVER']['hostname']
bssid_area = []
scanning_interface = config['SCAN']['wifi_interface']
token = config['SERVER']['token']
telegram_token = "bot123:xxx"
telegram_chat_id = ""
scanner_name = ""
#####################################

if verbose == "true":
    print("Jaaaa")
print(verbose)


def saveThread(q):
    time.sleep(5)
    while True:
        uploadData = q.get()
        if len(uploadData) > 0:
            try:
                response = requests.post('https://' + core_instance + '/api/v1/scan', json=uploadData,
                                         headers={'Authentication': token})
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " [SaveScan]: " + response.text)
            except Exception:
                print("Error on save. Retry.")
                q.put(uploadData)


def handleScan(qHandle, qSave):
    while True:
        cells = qHandle.get()
        uploadData = []
        for cell in cells:
            if cell.address not in found:
                found.append(cell.address)

                if True:  # proceed:
                    uploadData.append({
                        'bssid': cell.address,
                        'ssid': cell.ssid,
                        'signal': cell.signal,
                        'quality': cell.quality,
                        'frequency': cell.frequency.replace(" GHz", ""),
                        'encrypted': cell.encrypted == True,
                        'channel': cell.channel,
                        # 'latitude': 52.0,
                        # 'longitude': 9.0,
                        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
        qSave.put(uploadData)


qSave = queue.Queue()
qHandle = queue.Queue()

saveT = threading.Thread(target=saveThread, args=(qSave,))
saveT.start()

handleT = threading.Thread(target=handleScan, args=(qHandle, qSave,))
handleT.start()

i = 0
found = []
while True:
    i += 1
    if i > 60 * 10:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " [Main]: Laufzeit erreicht.")
        i = 1
        found = []
    try:
        cells = Cell.all(scanning_interface)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " [Main]: Scan... (" + str(
            qHandle.qsize()) + " Scans zu verarbeiten, )")
        qHandle.put(cells)
        time.sleep(0.2)
    except Exception as e:
        print(e)
        time.sleep(0.1)
