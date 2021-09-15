# Portscanner

## Table of Contents

* [Disclaiemr](#disclaimer)
* [About the Project](#about-the-project)
* [Usage](#usage)


## Disclaimer
This project is for educational purposes only. Don't use this for illegal activities. 
You are the only responsible for your actions.

## About The Project
As mentioned above this portscanner was created for educational purposes as I wanted a 
small python project to work on. 

This portscanner hast multithreading and has a progressbar to track how much of the scan is done. To do a full scan, all 65536 ports takes for me just over 1 hour.
<img width="1746" alt="Screenshot 2021-09-15 at 13 49 37" src="https://user-images.githubusercontent.com/47121010/133428098-94983110-88da-4140-8e68-df223ee8d91f.png">

Port Scanning is actively looking for open ports on a host or system to then possibly use for a exploit or attack on that system.
[More on portscanners](https://en.wikipedia.org/wiki/Port_scanner)

## Usage
```
usage: portscanner.py [-h] [-s STARTPORT] [-e ENDPORT] host

positional arguments:
  host                  Hostname or IP of host system to be scanned

optional arguments:
  -h, --help            show this help message and exit
  -s STARTPORT, --startPort STARTPORT
                        Port number to start scan (0-65535)
  -e ENDPORT, --endPort ENDPORT
                        Port number to end scan (0-65535)
```
