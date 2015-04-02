# hpupdater.py
# V0.0.1
# Thomas Attree

# Import dependancies
import ilo
import spp
import oa
from optparse import OptionParser

def main():
	# Option parser
	usage = ('usage: %prog -i <iLO upgrade mode> -s <Server firmware upgrade mode> -o <OA firmware upgrade mode>')
	parser = OptionParser(usage=usage)
	parser.add_option('-i', dest='ilo', action="store_true", help='Run in iLO upgrade mode', default=False)
	parser.add_option('-s', dest='server', action="store_true", help='Run server upgrade with offline SPP', default=False)
	parser.add_option('-o', dest='oa', action="store_true", help='Run Onboard Administrator upgrade', default=False)
	(options, args) = parser.parse_args()

	# Set mode based on option
	iloMode = options.ilo
	serverMode = options.server
	oaMode = options.oa

	# Sum counts True values
	onlyOne = sum([iloMode, serverMode, oaMode])

	# Check only one option is true
	if (onlyOne != 1):
		print (parser.usage)
		print ('[!] Please select only one operating mode\n')
		exit(0)
	# Now check which option is true
	elif (iloMode == True):
		# Execute ilo upgrade script
		print ('-------------------------------')
		print ('[*] Entering iLO upgrade script')
		print ('-------------------------------')
		ilo.main()
	elif (serverMode == True):
		# Execute SPP upgrade script
		print ('-------------------------------')
		print ('[*] Entering SPP upgrade script')
		print ('-------------------------------')
		spp.main()
	elif (oaMode == True):
		# Execute oa upgrade script
		print ('-------------------------------------------------')
		print ('[*] Entering Onboard Administrator upgrade script')
		print ('-------------------------------------------------')
		oa.main()


if __name__ == '__main__':
	main()
