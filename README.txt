HP Firmware updater
===================
Written by: Thomas Attree
thomas.j.attree@thomsonreuters.com

This set of scripts will upgrade HP iLO firmware, OA firmware
and HP Proliant servers with a HP provided SPP image.

Dependencies
------------
Python v2.6.6 (minimum)
Paramiko - A Python implementation of SSHv2
	http://www.paramiko.org

Usage
-----
Start by running hpupdater.py in one of the three modes:
	-i Upgrades iLO targets to desired versions using parameters
	   provided in ilo.conf

	-s Upgrades servers with a HP SPP ISO image. This performs
	   the upgrade in offline mode by mounting the ISO from an
	   external HTTP server. Parameters are set in spp.conf

	-o Upgrades HP OA firmware by running a self contained FTP
	   server. Parameters are specified in the oa.conf file.

Third party packages
--------------------
Paramiko - http://www.paramiko.org
GNU GPL v2.1
	Used in oa.py to establish SSH connections.

python-hpilo - https://github.com/seveas/python-hpilo
GNU GPL v3
	Used to connect to iLO devices in ilo.py and spp.py

License
-------
Released under GNU GPL V3
