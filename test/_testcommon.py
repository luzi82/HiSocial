import httplib
import install_config
import json
import unittest
import base.Command
import os.path
from hisocial.common import hs_random, hs_mime

OWNER_USERNAME="akari"
OWNER_PASSWORD="mizunashi"

WEB_JSON_CGI_URL_PATH="json-cgi"
WEB_JSON_CONSOLE_URL_PATH="json-console"
WEB_URL_PATH=""

class HsTest(unittest.TestCase):
    
    def call_web_json(self,value):
        output_name,data = self._call_web(value,"json_cmd.py")
        data = json.loads(data)
        return data

    def call_web_json_ok(self,value):
        data = self.call_web_json(value)
        self.assertEqual(data[base.Command.RESULT_KEY], base.Command.RESULT_VALUE_OK_TXT)
        return data

    def call_web_raw(self,value):
        output_name,data = self._call_web(value,"file.py")
        return output_name,data

    def _call_web(self,value,suffix):
        v_map = { \
           "root_path":install_config.ROOT_PATH, \
           "json_cgi":WEB_JSON_CGI_URL_PATH, \
           "suffix":suffix
        }
        url = "%(root_path)s/%(json_cgi)s/%(suffix)s" % v_map
        
        content_type, body = self._encode_multipart_formdata(value)
        
        h = httplib.HTTP(install_config.DOMAIN)
        h.putrequest('POST', url)
        h.putheader('Host', install_config.DOMAIN)
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        
        self.assertEqual(errcode,200)
        
        if "Content-Disposition" in headers:
            pfx = "attachment; filename="
            tmp = headers["Content-Disposition"]
            self.assertTrue(tmp.startswith(pfx))
            output_name = tmp[len(pfx):]
        else:
            output_name = None
        
        data = h.file.read()
        return output_name,data

    def _encode_multipart_formdata(self,value):
        # ref: http://code.activestate.com/recipes/146306-http-client-to-post-using-multipartform-data/
        BOUNDARY = hs_random.random_hex(64)
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
                L.append('Content-Type: %s' % hs_mime.read_file(v.name))
                L.append('')
                L.append(vbin)
            else:
                self.fail()
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def check_ok(self,result):
        self.assertTrue(result != None)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result["result"],base.Command.RESULT_VALUE_OK_TXT)

    def check_fail(self,result):
        self.assertTrue(result != None)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result["result"],base.Command.RESULT_VALUE_FAIL_TXT)
