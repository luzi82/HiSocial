import httplib
import install_config
import json
import unittest
import urllib
import pprint

OWNER_USERNAME="akari"
OWNER_PASSWORD="mizunashi"

class HsTest(unittest.TestCase):
    
    def call_web(self,value):
        v_map = { \
           "root_path":install_config.ROOT_PATH, \
           "json_cgi":install_config.WEB_JSON_CGI_URL_PATH \
        }
        params = urllib.urlencode(value)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(install_config.DOMAIN)
        conn.request("POST", "%(root_path)s/%(json_cgi)s/json_cmd.py" % v_map, params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        self.assertEqual(200, response.status)
        data = json.loads(data)
        return data

    def call_web_file(self,value):
        v_map = { \
           "root_path":install_config.ROOT_PATH, \
           "json_cgi":install_config.WEB_JSON_CGI_URL_PATH \
        }
        params = urllib.urlencode(value)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(install_config.DOMAIN)
        conn.request("POST", "%(root_path)s/%(json_cgi)s/file.py" % v_map, params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        self.assertEqual(200, response.status)
        return data
