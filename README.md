# simp
Monitor ICMP and SNMP


Hello All,

This is one of my projects.
This project monitor with SNMP and ICMP devices.
Feel free to customize it as you like.

The function numbers is used for troubleshoot using log file and here is a brief description for each function:
001 - Creating sqlite3 database.
002 - Generating logs.
003 - Send emails (You have to change the parameters).
004 - Monitor SNMP.
005 - Send ICMP.
006 - Take all the hosts from database and start monitoring them.
007 - Display all database values (Devices, ports, etc..)
008 - Adding new device for monitoring - Frontend.
009 - Adding a record of the device - Backend.
010 - See if ICMP is checked while adding new device.
010 - See if SNMP is checked while adding new device.

In order to make it work you should run 2 threads:
1. Main.py
2. WebUI.py

I still investigating multiprocessing and multithreading in python and this is why I didn't use here in this project.
For any issue or explanation you can send Email to: github.bar@gmail.com

Enjoy and be nice and patient to each other :)
