import os
import sys

my_path = os.path.abspath(__file__)
hisocial_root_path = os.path.dirname(os.path.dirname(my_path))
sys.path.insert(0, hisocial_root_path + "/core")

from admin import reset
from base import Runtime
try:
    import install_config
except ImportError:
    print "install_config.py not found"


do_reset = False
do_trace = False

if __name__ == '__main__':
#    parser = OptionParser()
#    parser.add_option("-p", "--password", dest="password", help="password")
#    (options, args) = parser.parse_args()
#    if(options.password != core_config.ADMIN_PASSWORD):
#        print("Wrong password")
#        quit()
    do_trace = True
    do_reset = True
elif __name__ == "reset_all":
    do_reset = True
    
if do_reset:
    Runtime.enable_trace=do_trace
    reset.reset(install_config)
