#!/usr/bin/python

from Crypto.Util.randpool import RandomPool
import binascii
import os
import runpy
try:
    import install_config
except ImportError:
    print "install_config.py not found"
    
# default

DEFAULT_USER_ID_LENGTH_MIN = 4
DEFAULT_USER_ID_LENGTH_MAX = 100
DEFAULT_USER_PASSWORD_LENGTH_MIN = 4
DEFAULT_USER_PASSWORD_LENGTH_MAX = 100
DEFAULT_USER_TOKEN_VALID_TIME_PERIOD = 10 * 60

# enviroment

my_path=os.path.abspath(__file__)
hisocial_root_path=os.path.dirname(os.path.dirname(my_path))

# func

randompool = RandomPool()
def random_hex(size):
    b=randompool.get_bytes(size/2)
    return binascii.b2a_hex(b)

# core/core_config.py

core_config_filename=hisocial_root_path+"/core/core_config.py"
try: os.unlink(core_config_filename)
except OSError: pass
core_config_file = open(core_config_filename,"w")

core_config_file.writelines([
    "DB_SERVER = \'%s\'\n" % install_config.DB_SERVER,
    "DB_USERNAME = \'%s\'\n" % install_config.DB_USERNAME,
    "DB_PASSWORD = \'%s\'\n" % install_config.DB_PASSWORD,
    "DB_SCHEMATA = \'%s\'\n" % install_config.DB_SCHEMATA,
    "USER_ID_LENGTH_MIN = %d\n" % DEFAULT_USER_ID_LENGTH_MIN,
    "USER_ID_LENGTH_MAX = %d\n" % DEFAULT_USER_ID_LENGTH_MAX,
    "USER_PASSWORD_LENGTH_MIN = %d\n" % DEFAULT_USER_PASSWORD_LENGTH_MIN,
    "USER_PASSWORD_LENGTH_MAX = %d\n" % DEFAULT_USER_PASSWORD_LENGTH_MAX,
    "USER_TOKEN_ENC_KEY = \'%s\'\n" % random_hex(32),
    "USER_TOKEN_HASH_HMAC = \'%s\'\n" % random_hex(32),
    "USER_TOKEN_VALID_TIME_PERIOD = %d\n" % DEFAULT_USER_TOKEN_VALID_TIME_PERIOD,
    "USER_ACCOUNT_PASSWORD_HMAC = \'%s\'\n" % random_hex(32),
    "RECAPTCHA_PUBLIC_KEY = \'%s\'\n" % install_config.RECAPTCHA_PUBLIC_KEY,
    "RECAPTCHA_PRIVATE_KEY = \'%s\'\n" % install_config.RECAPTCHA_PRIVATE_KEY
])

core_config_file.close()

# web-json-cgi/webjsoncgi_config.py

webjsoncgi_config_filename=hisocial_root_path+"/web-json-cgi/webjsoncgi_config.py"
try: os.unlink(webjsoncgi_config_filename)
except OSError: pass
webjsoncgi_config_file = open(webjsoncgi_config_filename,"w")

webjsoncgi_config_file.writelines([
    "CORE_PATH = \'%s\'\n" % (hisocial_root_path+"/core")
])

webjsoncgi_config_file.close()

# web-json-console/webjsonconsole_config.js

webjsonconsole_config_filename=hisocial_root_path+"/web-json-console/webjsonconsole_config.js"
try: os.unlink(webjsonconsole_config_filename)
except OSError: pass
webjsonconsole_config_file = open(webjsonconsole_config_filename,"w")

webjsonconsole_config_file.writelines([
    "var HISOCIAL_JSON_URL = \'%s\';\n" % (install_config.URL_ROOT+"/"+install_config.WEB_JSON_CGI_URL_PATH+"/json_cmd.py"),
    "var RECAPTCHA_PUBLIC_KEY = \'%s\';\n" % (install_config.RECAPTCHA_PUBLIC_KEY)
])

webjsonconsole_config_file.close()

# install web-json-cgi

try: os.makedirs(os.path.dirname(install_config.WEB_JSON_CGI_LOCAL_PATH))
except OSError: pass
try: os.unlink(install_config.WEB_JSON_CGI_LOCAL_PATH)
except OSError: pass
os.symlink(hisocial_root_path+"/web-json-cgi",install_config.WEB_JSON_CGI_LOCAL_PATH)

# install json-console

try: os.makedirs(os.path.dirname(install_config.WEB_JSON_CONSOLE_LOCAL_PATH))
except OSError: pass
try: os.unlink(install_config.WEB_JSON_CONSOLE_LOCAL_PATH)
except OSError: pass
os.symlink(hisocial_root_path+"/web-json-console",install_config.WEB_JSON_CONSOLE_LOCAL_PATH)

# reset everything

runpy.run_module("reset_all")
