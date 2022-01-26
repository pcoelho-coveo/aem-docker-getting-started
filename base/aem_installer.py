import sys
import helpers
from optparse import OptionParser

# Argument definition
usage = "usage: %prog [options] arg"
parser = OptionParser(usage)
parser.add_option("-i", "--install_file", dest="file_name", help="AEM install file")
parser.add_option("-r", "--runmode", dest="run_mode", help="Run mode for the installation")
parser.add_option("-p", "--port", dest="port", help="Port for instance")

options, args = parser.parse_args()
option_dic = vars(options)
file_name = option_dic.setdefault('file_name', 'cq-publish-4503.jar')
run_mode = option_dic.setdefault('run_mode', 'publish')
port = option_dic.setdefault('port', '4503')

# Copy out parameters
helpers.log("aem_installer.py called with params: %s" % option_dic)

helpers.import_packages(file_name, port, run_mode)

sys.exit(0)
