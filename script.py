from wifi import Cell, Scheme
import datetime
import time
import requests

found = []

while True:
	try:
		print(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ": Scan...")
		cells = Cell.all('wlan0')
		for cell in cells:
			if cell.address not in found:
				print(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ": " + cell.address + " " + cell.ssid)
				found.append(cell.address)
				response = requests.get('https://xxx' + cell.address)
				print(response.text)
		time.sleep(1)
	except Exception as e:
		print(e)
		time.sleep(5)
