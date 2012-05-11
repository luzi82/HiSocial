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
DEFAULT_USER_TOKEN_VALID_TIME_PERIOD = 7 * 24 * 60 * 60

# enviroment

my_path=os.path.abspath(__file__)
hisocial_root_path=os.path.dirname(os.path.dirname(my_path))

# path

URL_ROOT="http://%(domain)s%(path)s"%{"domain":install_config.DOMAIN,"path":install_config.ROOT_PATH}

DATA_FOLDER=install_config.HISOCIAL_ROOT+"/data"

WEB_JSON_CGI_LOCAL_PATH=install_config.HISOCIAL_ROOT+"/www/json-cgi"
WEB_JSON_CGI_URL_PATH="json-cgi"

WEB_JSON_CONSOLE_LOCAL_PATH=install_config.HISOCIAL_ROOT+"/www/json-console"
WEB_JSON_CONSOLE_URL_PATH="json-console"

WEB_LOCAL_PATH=install_config.HISOCIAL_ROOT+"/www/root"
WEB_URL_PATH=""

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
    "DATA_FOLDER = \'%s\'\n" % DATA_FOLDER,
    "USER_ID_LENGTH_MIN = %d\n" % DEFAULT_USER_ID_LENGTH_MIN,
    "USER_ID_LENGTH_MAX = %d\n" % DEFAULT_USER_ID_LENGTH_MAX,
    "USER_PASSWORD_LENGTH_MIN = %d\n" % DEFAULT_USER_PASSWORD_LENGTH_MIN,
    "USER_PASSWORD_LENGTH_MAX = %d\n" % DEFAULT_USER_PASSWORD_LENGTH_MAX,
    "USER_TOKEN_ENC_KEY = \'%s\'\n" % random_hex(32),
    "USER_TOKEN_HASH_HMAC = \'%s\'\n" % random_hex(32),
    "USER_TOKEN_VALID_TIME_PERIOD = %d\n" % DEFAULT_USER_TOKEN_VALID_TIME_PERIOD,
    "USER_ACCOUNT_PASSWORD_HMAC = \'%s\'\n" % random_hex(32),
    "RECAPTCHA_PUBLIC_KEY = \'%s\'\n" % install_config.RECAPTCHA_PUBLIC_KEY,
    "RECAPTCHA_PRIVATE_KEY = \'%s\'\n" % install_config.RECAPTCHA_PRIVATE_KEY,
    "HIFILE_ENC_KEY = \'%s\'\n" % random_hex(32),
    "HIFILE_HASH_HMAC = \'%s\'\n" % random_hex(32),
    "FILE_TOKEN_ENC_KEY = \'%s\'\n" % random_hex(32),
    "FILE_TOKEN_HASH_HMAC = \'%s\'\n" % random_hex(32),
    "TEST_KEY = \'%s\'\n" % (random_hex(64) if install_config.TEST_ENABLE else ""),
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
    "var HISOCIAL_JSON_URL = \'%s\';\n" % (URL_ROOT+"/"+WEB_JSON_CGI_URL_PATH+"/json_cmd.py"),
    "var RECAPTCHA_PUBLIC_KEY = \'%s\';\n" % (install_config.RECAPTCHA_PUBLIC_KEY)
])

webjsonconsole_config_file.close()

# web/web_config.js

web_config_filename=hisocial_root_path+"/web/web_config.js"
try: os.unlink(web_config_filename)
except OSError: pass
web_config_file = open(web_config_filename,"w")

web_config_file.writelines([
    "var HISOCIAL_JSON_URL = \'%s\';\n" % (URL_ROOT+"/"+WEB_JSON_CGI_URL_PATH+"/json_cmd.py"),
    "var HISOCIAL_FILE_URL = \'%s\';\n" % (URL_ROOT+"/"+WEB_JSON_CGI_URL_PATH+"/file.py"),
    "var RECAPTCHA_PUBLIC_KEY = \'%s\';\n" % (install_config.RECAPTCHA_PUBLIC_KEY)
])

web_config_file.close()

# install web-json-cgi

try: os.makedirs(os.path.dirname(WEB_JSON_CGI_LOCAL_PATH))
except OSError: pass
try: os.unlink(WEB_JSON_CGI_LOCAL_PATH)
except OSError: pass
os.symlink(hisocial_root_path+"/web-json-cgi",WEB_JSON_CGI_LOCAL_PATH)

# install web-json-console

try: os.makedirs(os.path.dirname(WEB_JSON_CONSOLE_LOCAL_PATH))
except OSError: pass
try: os.unlink(WEB_JSON_CONSOLE_LOCAL_PATH)
except OSError: pass
os.symlink(hisocial_root_path+"/web-json-console",WEB_JSON_CONSOLE_LOCAL_PATH)

# install web

try: os.makedirs(os.path.dirname(WEB_LOCAL_PATH))
except OSError: pass
try: os.unlink(WEB_LOCAL_PATH)
except OSError: pass
os.symlink(hisocial_root_path+"/web",WEB_LOCAL_PATH)

# debian-lighttpd

hiauntie_mod_filename = install_config.HISOCIAL_ROOT+"/system/debian-lighttpd/99-hiauntie.conf"
try: os.makedirs(os.path.dirname(hiauntie_mod_filename))
except OSError: pass
try: os.unlink(hiauntie_mod_filename)
except OSError: pass
hiauntie_mod_file = open(hiauntie_mod_filename,"w")
hiauntie_mod_file.write( \
'''static-file.exclude-extensions += ( ".py " )

alias.url += ( "%(WEB_JSON_CGI_URL_PATH)s" => "%(WEB_JSON_CGI_LOCAL_PATH)s" )
$HTTP["url"] =~ "^%(WEB_JSON_CGI_URL_PATH)s/" {
    cgi.assign += ( ".py" => "/usr/bin/python" )
    dir-listing.activate = "disable"
}
$HTTP["url"] =~ "^%(WEB_JSON_CGI_URL_PATH)s/webjsoncgi_config.py$" { url.access-deny = ("") }

alias.url += ( "%(WEB_JSON_CONSOLE_URL_PATH)s" => "%(WEB_JSON_CONSOLE_LOCAL_PATH)s" )
$HTTP["url"] =~ "^%(WEB_JSON_CONSOLE_URL_PATH)s/" {
    dir-listing.activate = "disable"
}
''' % { \
    "WEB_JSON_CGI_URL_PATH":install_config.ROOT_PATH+"/"+WEB_JSON_CGI_URL_PATH, \
    "WEB_JSON_CGI_LOCAL_PATH":WEB_JSON_CGI_LOCAL_PATH, \
    "WEB_JSON_CONSOLE_URL_PATH":install_config.ROOT_PATH+"/"+WEB_JSON_CONSOLE_URL_PATH, \
    "WEB_JSON_CONSOLE_LOCAL_PATH":WEB_JSON_CONSOLE_LOCAL_PATH, \
}
)
hiauntie_mod_file.close()

# reset everything

runpy.run_module("reset_all")
