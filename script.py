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

verbose = config['SCRIPT']['verbose']
core_instance = config['SERVER']['hostname']
scanning_interface = config['SCAN']['wifi_interface']
token = config['SERVER']['token']


def verbose(thread, message):
    if verbose == "true":
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " [" + thread + "]: " + message)


def saveThread(q):
    time.sleep(5)
    while True:
        uploadData = q.get()
        if len(uploadData) > 0:
            try:
                response = requests.post('https://' + core_instance + '/api/v1/scan', json=uploadData,
                                         headers={'Authentication': token})
                verbose("SaveScan", response.text)
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
                uploadData.append({
                    'bssid': cell.address,
                    'ssid': cell.ssid,
                    'signal': cell.signal,
                    'quality': cell.quality,
                    'frequency': cell.frequency.replace(" GHz", ""),
                    'encrypted': cell.encrypted == True,
                    'channel': cell.channel,
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
        verbose("Main", "Laufzeit erreicht.")
        i = 1
        found = []
    try:
        cells = Cell.all(scanning_interface)
        verbose("Main", "Scan... (" + str(qHandle.qsize()) + " Scans zu verarbeiten, )")
        qHandle.put(cells)
        time.sleep(0.2)
    except Exception as e:
        print(e)
        time.sleep(0.1)
