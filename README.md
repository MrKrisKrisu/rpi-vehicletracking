# Vehicletracking Python Scanner

This script scans for wifi networks and sends their information to a remote server via HTTP POST requests. The script is
written in Python 3 and uses the following libraries: datetime, queue, threading, time, configparser, requests, socket,
and wifi.

> You need an instance of [vehicletracking-core](https://github.com/MrKrisKrisu/vehicletracking-core) to use this
> script.

# Installation

1. Make sure Python 3 is installed on your system.
2. Clone this repository: `git clone https://github.com/MrKrisKrisu/rpi-vehicletracking.git`
3. Install the required libraries: `pip install -r requirements.txt`
4. Set up the configuration file by copying the config.example.ini file to config.ini and filling in the necessary
   values.
5. Run the script: `python script.py`

# Usage

When the script is running, it will continuously scan for wifi networks using the specified wifi interface and push any
new networks it finds to a remote server. The script will also log its activities to the console if logging is enabled
in the configuration file.

The script consists of three threads:

Main thread: starts the other threads and logs its activities.

Scan thread: scans for wifi networks and adds new networks to a queue.

Save thread: sends network information to the remote server via HTTP POST requests.
If the script loses internet connection, it will wait for 5 seconds and then attempt to send the data again. If the
connection is still not available, the script will keep attempting to send the data every 5 seconds until it succeeds.

# Configuration

The script's configuration is stored in a `config.ini` file, which contains the following sections and options:

- `SCRIPT`
    - `verbose`: if set to "true", the script will log its activities to the console.
- `SERVER`
    - `hostname`: the hostname of the remote server to which the script will send network information.
    - `token`: the authentication token to be used in the HTTP POST requests.
- `SCAN`
    - `wifi_interface`: the name of the wifi interface to be used for scanning.
    - `scan_interval`: the interval in seconds between each scan.