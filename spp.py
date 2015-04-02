# ilo.py
# Part of hpupdater
# V0.0.1
# Thomas Attree

import hpilo
import hpilo_fw
import ConfigParser
import time

def print_progress(text):
	sys.stdout.write('\r\033[K' + text)
	sys.stdout.flush()

def spp(target, login, password, url, key):
	ilo = hpilo.Ilo(target, login, password)
	print ('[+] Applying SPP to ' + target)
	#check if anything mounted get_vm_status(device='CDROM')
	#if not install the key
	try:	
		media_state = (ilo.get_vm_status(device='CDROM')['image_inserted'])
		#print media_state
	except:
		ilo.activate_license(key)
		media_state = (ilo.get_vm_status(device='CDROM')['image_inserted'])
		print ('[+] iLO Advanced was not present but has been applied to ' + target)

	#dismount anything that might already be there eject_virtual_media(device='cdrom')
	if media_state == 'YES':
		ilo.eject_virtual_media(device='cdrom')

	#mount cdrom to url insert_virtual_media(cdrom, url)
	try:
		ilo.insert_virtual_media('cdrom', url)
	except:
		print ('******************************')
		print ('[-] Could not insert media on ' + target)
		print ('******************************')
		return

	#set boot set_vm_status(device='cdrom', boot_option='boot_once', write_protect=True
	try:
		ilo.set_vm_status(device='cdrom', boot_option='boot_once', write_protect=True)
	except:
		print ('******************************')
		print ('[-] Could not set boot status on ' + target)
		print ('******************************')
		return

	#check if server is on get_host_power_status()
	power = ilo.get_host_power_status()
	#print power

	#if off boot server press_pwr_btn()
	if power == 'OFF':
		ilo.press_pwr_btn()
	elif power == 'ON':
		print ('[-] ' + target + ' is currently powered on')
		print ('    Attempting ACPI shutdown')
		ilo.press_pwr_btn()
		print ('[*] Waiting 60 seconds')
		if 	ilo.get_host_power_status() == 'OFF':
			print ('[-] ACPI shutdown unsuccessful')
			print ('[!] Forcing cold boot')
			ilo.cold_boot_server()


def main():
	# Grab the config from spp.conf
	config = ConfigParser.ConfigParser()
	try:
			config.read('spp.conf')
			targets = config.get('targets', 'target').split(',')
			login = config.get('credentials', 'username')
			password = config.get('credentials', 'password')
			url = config.get('spp_url', 'spp')
			key = config.get('license', 'key')
	except:
		print ('[-] Unable read config settings from spp.conf')
		print ('    Please verify spp.conf and try again')

	# Print out contents of spp.conf for review
	print ('[*] The following parameters will be used:')
	print ('    Username: ' + login)
	print ('    Password: ' + password)
	print ('    iLO Advanced key (if needed): ' + key)
	print ('[*] The following IP\'s will be targetd for upgrade:')
	for ip in targets:
		print ('    ' + ip)
	print ('[*] This amounts to ' + str(len(targets)) + ' systems in total')
	print ('[*] This operation should take approximately ' + str((len(targets) * 300)/60)\
			+ ' minutes to complete')

	# Get confirmation from user
	print ('[!] Are you sure you want to continue?')
	userConfirm = raw_input("    Type YES to continue:")

	# If confirmed update servers!
	if userConfirm == 'YES' or userConfirm == 'yes':
		for ip in targets:
			spp(ip, login, password, url, key)
			print ('[*] Waiting 5 minutes as to not clog management network')
			time.sleep(300)
		print ('[+] All target hosts contacted and SPP mounted')
	else:
		print ('[-] Servers will not be upgraded. Exiting script')
		exit(0)


if __name__ == '__main__':
	main()
