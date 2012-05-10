import httplib
import install_config
import json
import unittest
import urllib
import pprint
import base.Command
from Crypto.Util.randpool import RandomPool
import binascii
import os.path
import base.MimeDetection

OWNER_USERNAME="akari"
OWNER_PASSWORD="mizunashi"

class HsTest(unittest.TestCase):
    
    def call_web(self,value):
        v_map = { \
           "root_path":install_config.ROOT_PATH, \
           "json_cgi":install_config.WEB_JSON_CGI_URL_PATH \
        }
        url = "%(root_path)s/%(json_cgi)s/json_cmd.py" % v_map
        
        content_type, body = self._encode_multipart_formdata(value)
        
        h = httplib.HTTP(install_config.DOMAIN)
        h.putrequest('POST', url)
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        
        self.assertEqual(errcode,200)
        
        data = h.file.read()
        data = json.loads(data)
        return data
        
    def call_web_ok(self,value):
        data = self.call_web(value)
        self.assertEqual(data[base.Command.RESULT_KEY], base.Command.RESULT_VALUE_OK_TXT)
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

    def _encode_multipart_formdata(self,value):
        # ref: http://code.activestate.com/recipes/146306-http-client-to-post-using-multipartform-data/
        BOUNDARY = random_hex(64)
        CRLF = '\r\n'
        L = []
        for k in value:
            v = value[k]
            if isinstance(v,str):
                L.append('--' + BOUNDARY)
                L.append('Content-Disposition: form-data; name="%s"' % k)
                L.append('')
                L.append(v)
            elif isinstance(v,file):
                vbin = v.read()
                v.close()
                L.append('--' + BOUNDARY)
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (k, os.path.basename(v.name)))
                L.append('Content-Type: %s' % base.MimeDetection.read_file(v.name))
                L.append('')
                L.append(vbin)
            else:
                self.fail()
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

randompool = RandomPool()
def random_hex(size):
    b=randompool.get_bytes(size/2)
    return binascii.b2a_hex(b)
