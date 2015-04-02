# ilo.py
# Part of hpupdater
# V0.0.1
# Thomas Attree

# Import dependencies
import hpilo
import hpilo_fw
import time
import ConfigParser

def print_progress(text):
	sys.stdout.write('\r\033[K' + text)
	sys.stdout.flush()

def ilo3_128(hostname, login, password, ilo3):
	print ('[+] Upgrading ' + hostname + ' to v1.28')
	ilobin = 'ilo3_128.bin'
	ilo = hpilo.Ilo(hostname, login, password)
	ilo.update_rib_firmware(filename='ilobins/' + ilobin, progress=print_progress)
	print ('\n[*] Waiting 2 Minutes for iLO to reset before upgrading to ' + ilo3)
	time.sleep(120)
	return

def ilogo(hostname, login, password, ilo2, ilo3, ilo4):
	# Set the iLo variable
	ilo = hpilo.Ilo(hostname, login, password)
	
	#Check current iLO version
	try:
		ilo_fw_version = ilo.get_fw_version()
	except:
		print ('[-] Cannot connect to ' + hostname)
		return

	ilo_version = ilo_fw_version['management_processor']
	firmware_version = ilo_fw_version['firmware_version']
	print ('[*] Checking ' + hostname)	
	print ('[*] iLO type: ' + ilo_version)
	print ('[*] Current firmware: ' + firmware_version)

	checkilo = ilo_version.lower() + '_' + firmware_version.replace('.', '') + '.bin'
	#print (checkilo)

	if checkilo == ilo2 or 	checkilo == ilo3 or checkilo == ilo4:
		print ('[+] Current firmare at target version')
	else:
		print ('[-] Firmware will be updated')
		if ilo_version == 'iLO2':
			ilobin = ilo2

		elif ilo_version == 'iLO3':
			# Problems upgrading from versions before 1.28
			# if ilo3 lower than 1.28 detected, force upgrade to 1.28 first
			if float(firmware_version) < 1.28:
				print ('[-] Current version too old.')
				print ('    ' + hostname + ' MUST upgrade to v1.28 before proceeding')
				ilo3_128(hostname, login, password, ilo3)
			ilobin = ilo3

		elif ilo_version == 'iLO4':
			ilobin = ilo4

		print ('[+] Updating ' + hostname)
		try:
			ilo.update_rib_firmware(filename= 'ilobins/' + ilobin, progress=print_progress)
		except:
			print ('\n[-] An error occured whilst updating ' + hostname)
			print ('\n    Please try this host again')
		print('')


def main():
	# Grab the config from ilo.conf
	config = ConfigParser.ConfigParser()
	try:
			config.read('ilo.conf')
			targets = config.get('targets', 'target').split(',')
			login = config.get('credentials', 'username')
			password = config.get('credentials', 'password')
			ilo2 = config.get('ilo_file', 'ilo2')
			ilo3 = config.get('ilo_file', 'ilo3')
			ilo4 = config.get('ilo_file', 'ilo4')
	except:
			print ('[-] Unable read config settings from ilo.conf')
			print ('    Please verify ilo.conf and try again')

	# Print out contents of ilo.conf for review
	print ('[*] The following parameters will be used:')
	print ('    Username: ' + login)
	print ('    Password: ' + password)
	print ('    iLO2 Version: ' + ilo2)
	print ('    iLO3 Version: ' + ilo3)
	print ('    iLO4 Version: ' + ilo4)
	print ('[*] The following IP\'s will be targetd for upgrade:')
	for ip in targets:
		print ('    ' + ip)
	print ('[*] This amounts to ' + str(len(targets)) + ' systems in total')

	# Get confirmation from user
	print ('[!] Are you sure you want to continue?')
	userConfirm = raw_input("    Type YES to continue:")

	# If confirmed update ilos!
	if userConfirm == 'YES' or userConfirm == 'yes':
		for ip in targets:
			ilogo(ip, login, password, ilo2, ilo3, ilo4) 
	else:
		print ('[-] iLO\'s will not be upgraded. Exiting script')
		exit(0)
	

if __name__ == '__main__':
	main()
