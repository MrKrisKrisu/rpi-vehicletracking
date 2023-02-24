#!/usr/bin/python3 -u

import datetime
import queue
import threading
import time
import configparser
import requests
import socket
from wifi import Cell

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

verbose = config['SCRIPT']['verbose']
core_instance = config['SERVER']['hostname']
scanning_interface = config['SCAN']['wifi_interface']
token = config['SERVER']['token']
scan_interval = float(config['SCAN']['scan_interval'])


def log(thread, message, force=False):
    if verbose == "true" or force:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " [" + thread + "]: " + message)


log("Main", "Starting script...", True)
log("Main", "____________________________________________", True)
log("Main", "Scanning interface " + scanning_interface, True)
log("Main", "Scanning every " + str(scan_interval) + " seconds", True)
log("Main", "Pushing to Host " + core_instance, True)
log("Main", "Logging is active? -> " + verbose, True)
log("Main", "____________________________________________", True)


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False


def saveThread(q):
    time.sleep(5)
    while True:
        log("SaveThread", str(q.qsize()) + " Uploads pending...")
        if internet():
            uploadData = q.get()
            if len(uploadData) > 0:
                try:
                    response = requests.post('https://' + core_instance + '/api/v1/scan', json=uploadData,
                                             headers={'Authentication': token})
                    log("SaveScan", response.text)
                except Exception:
                    log("SaveThread", "Error on save. Retry.", True)
                    q.put(uploadData)
                time.sleep(0.5)
        else:
            time.sleep(5)


def handleScan(qHandle, qSave):
    while True:
        cells = qHandle.get()
        uploadData = []
        for cell in cells:
            if cell.address not in found:
                log("ScanThread", "Found new network " + cell.address + " / " + cell.ssid)
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
        log("Main", "Runtime reached; Resetting list of networks")
        i = 1
        found = []
    try:
        log("Main", "Scan...")
        cells = Cell.all(scanning_interface)
        qHandle.put(cells)
        time.sleep(scan_interval)
    except Exception as e:
        log("Main", "Error: " + str(e), True)
        time.sleep(0.1)
