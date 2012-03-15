#!/usr/bin/python
"""
Simple example for an OpenID consumer.

Once you understand this example you'll know the basics of OpenID
and using the Python OpenID library. You can then move on to more
robust examples, and integrating OpenID into your application.
"""
__copyright__ = 'Copyright 2005-2008, Janrain, Inc.'

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from Cookie import SimpleCookie
from openid.consumer import consumer
from openid.cryptutil import randomString
from openid.extensions import pape, sreg
from openid.fetchers import setDefaultFetcher, Urllib2Fetcher
from openid.oidutil import appendArgs
from openid.store import filestore, memstore
import cgi
import cgitb
import sys
import urlparse
import StringIO
import os
import os.path
import time
import pickle
import openid

hostname="localhost"
uri_prefix="/~luzi82/HiSocial/test"
openid_store="/home/luzi82/ttt/openid/"
session_file="/home/luzi82/ttt/session.dat"

def quoteattr(s):
    qs = cgi.escape(s, 1)
    return '"%s"' % (qs,)

# Used with an OpenID provider affiliate program.
OPENID_PROVIDER_NAME = 'MyOpenID'
OPENID_PROVIDER_URL ='https://www.myopenid.com/affiliate_signup?affiliate_id=39'


#class OpenIDHTTPServer(HTTPServer):
#    """http server that contains a reference to an OpenID consumer and
#    knows its base URL.
#    """
#    def __init__(self, store, *args, **kwargs):
#        HTTPServer.__init__(self, *args, **kwargs)
#        self.sessions = {}
#        self.store = store
#
#        if self.server_port != 80:
#            self.base_url = ('http://%s:%s/' %
#                             (self.server_name, self.server_port))
#        else:
#            self.base_url = 'http://%s/' % (self.server_name,)

class FakeHeaders(object):
    
    environ = {}
    
    def set_environ(self,eee):
        ee={}
        for k,v in eee.iteritems():
            kk=k.lower()
            kk=kk.replace("_","-")
            if not kk.startswith("http-"):
                continue
            kk=kk[5:]
            ee[kk]=v
        self.environ=ee
    
    def get(self,k):
        if self.environ==None:
            return None
        kk = k.lower()
        if not kk in self.environ:
            return None
        return self.environ[kk]

class FakeServer(object):
    
    def __init__(self):
        self.sessions = {}
        self.store = filestore.FileOpenIDStore(openid_store)
        self.base_url = ('http://'+hostname+uri_prefix+'/')
    
# BaseHTTPRequestHandler
class OpenIDRequestHandler(object):
    """Request handler that knows how to verify an OpenID identity."""
    SESSION_COOKIE_NAME = 'pyoidconsexsid'

    session = None
    server = FakeServer()
    path = None
    user = None
    headers = None
    
    my_path=None

    wfile = StringIO.StringIO()

    def getConsumer(self, stateless=False):
        if stateless:
            store = None
        else:
            store = self.server.store
        return consumer.Consumer(self.getSession(), store)

    def getSession(self):
        """Return the existing session or a new session"""
        if self.session is not None:
            return self.session

        # Get value of cookie header that was sent
        cookie_str = self.headers.get('Cookie')
        if cookie_str:
            cookie_obj = SimpleCookie(cookie_str)
            sid_morsel = cookie_obj.get(self.SESSION_COOKIE_NAME, None)
            if sid_morsel is not None:
                sid = sid_morsel.value
            else:
                sid = None
        else:
            sid = None

        # If a session id was not set, create a new one
        if sid is None:
            sid = randomString(16, '0123456789abcdef')
            session = None
        else:
            session = self.server.sessions.get(sid)

        # If no session exists for this session ID, create one
        if session is None:
            session = self.server.sessions[sid] = {}

        session['id'] = sid
        self.session = session
        return session

    def setSessionCookie(self):
        sid = self.getSession()['id']
        session_cookie = '%s=%s;' % (self.SESSION_COOKIE_NAME, sid)
        self.send_header('Set-Cookie', session_cookie)

    def do_GET(self):
        """Dispatching logic. There are three paths defined:

          / - Display an empty form asking for an identity URL to
              verify
          /verify - Handle form submission, initiating OpenID verification
          /process - Handle a redirect from an OpenID server

        Any other path gets a 404 response. This function also parses
        the query parameters.

        If an exception occurs in this function, a traceback is
        written to the requesting browser.
        """
        try:
            self.parsed_uri = urlparse.urlparse(self.path)
            self.query = {}
            for k, v in cgi.parse_qsl(self.parsed_uri[4]):
                self.query[k] = v.decode('utf-8')

            path = self.parsed_uri[2]
            self.my_path=path
            if path == '/':
                self.render()
            elif path == '/verify':
                self.doVerify()
            elif path == '/process':
                self.doProcess()
            elif path == '/affiliate':
                self.doAffiliate()
            else:
                self.notFound()

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.setSessionCookie()
            self.end_headers()
            self.wfile.write(cgitb.html(sys.exc_info(), context=10))

    def doVerify(self):
        """Process the form submission, initating OpenID verification.
        """

        # First, make sure that the user entered something
        openid_url = self.query.get('openid_identifier')
        if not openid_url:
            self.render('Enter an OpenID Identifier to verify.',
                        css_class='error', form_contents=openid_url)
            return

        immediate = 'immediate' in self.query
        use_sreg = 'use_sreg' in self.query
        use_pape = 'use_pape' in self.query
        use_stateless = 'use_stateless' in self.query

        oidconsumer = self.getConsumer(stateless = use_stateless)
        try:
            request = oidconsumer.begin(openid_url)
        except consumer.DiscoveryFailure, exc:
            fetch_error_string = 'Error in discovery: %s' % (
                cgi.escape(str(exc[0])))
            self.render(fetch_error_string,
                        css_class='error',
                        form_contents=openid_url)
        else:
            if request is None:
                msg = 'No OpenID services found for <code>%s</code>' % (
                    cgi.escape(openid_url),)
                self.render(msg, css_class='error', form_contents=openid_url)
            else:
                # Then, ask the library to begin the authorization.
                # Here we find out the identity server that will verify the
                # user's identity, and get a token that allows us to
                # communicate securely with the identity server.
                if use_sreg:
                    self.requestRegistrationData(request)

                if use_pape:
                    self.requestPAPEDetails(request)

                trust_root = self.server.base_url
                return_to = self.buildURL('process')
                if request.shouldSendRedirect():
                    redirect_url = request.redirectURL(
                        trust_root, return_to, immediate=immediate)
                    self.send_response(302)
                    self.send_header('Location', redirect_url)
                    self.writeUserHeader()
                    self.end_headers()
                else:
                    form_html = request.htmlMarkup(
                        trust_root, return_to,
                        form_tag_attrs={'id':'openid_message'},
                        immediate=immediate)

                    self.wfile.write(form_html)

    def requestRegistrationData(self, request):
        sreg_request = sreg.SRegRequest(
            required=['nickname'], optional=['fullname', 'email'])
        request.addExtension(sreg_request)

    def requestPAPEDetails(self, request):
        pape_request = pape.Request([pape.AUTH_PHISHING_RESISTANT])
        request.addExtension(pape_request)

    def doProcess(self):
        """Handle the redirect from the OpenID server.
        """
        oidconsumer = self.getConsumer()

        # Ask the library to check the response that the server sent
        # us.  Status is a code indicating the response type. info is
        # either None or a string containing more information about
        # the return type.
#        url = 'http://'+self.headers.get('Host')+self.path
        url = 'http://'+self.headers.get('Host')+uri_prefix+self.path
        info = oidconsumer.complete(self.query, url)

        sreg_resp = None
        pape_resp = None
        css_class = 'error'
        display_identifier = info.getDisplayIdentifier()

        if info.status == consumer.FAILURE and display_identifier:
            # In the case of failure, if info is non-None, it is the
            # URL that we were verifying. We include it in the error
            # message to help the user figure out what happened.
            fmt = "Verification of %s failed: %s"
            message = fmt % (cgi.escape(display_identifier),
                             info.message)
        elif info.status == consumer.SUCCESS:
            # Success means that the transaction completed without
            # error. If info is None, it means that the user cancelled
            # the verification.
            css_class = 'alert'

            # This is a successful verification attempt. If this
            # was a real application, we would do our login,
            # comment posting, etc. here.
            fmt = "You have successfully verified %s as your identity."
            message = fmt % (cgi.escape(display_identifier),)
            sreg_resp = sreg.SRegResponse.fromSuccessResponse(info)
            pape_resp = pape.Response.fromSuccessResponse(info)
            if info.endpoint.canonicalID:
                # You should authorize i-name users by their canonicalID,
                # rather than their more human-friendly identifiers.  That
                # way their account with you is not compromised if their
                # i-name registration expires and is bought by someone else.
                message += ("  This is an i-name, and its persistent ID is %s"
                            % (cgi.escape(info.endpoint.canonicalID),))
        elif info.status == consumer.CANCEL:
            # cancelled
            message = 'Verification cancelled'
        elif info.status == consumer.SETUP_NEEDED:
            if info.setup_url:
                message = '<a href=%s>Setup needed</a>' % (
                    quoteattr(info.setup_url),)
            else:
                # This means auth didn't succeed, but you're welcome to try
                # non-immediate mode.
                message = 'Setup needed'
        else:
            # Either we don't understand the code or there is no
            # openid_url included with the error. Give a generic
            # failure message. The library should supply debug
            # information in a log.
            message = 'Verification failed.'

        self.render(message, css_class, display_identifier,
                    sreg_data=sreg_resp, pape_data=pape_resp)

    def doAffiliate(self):
        """Direct the user sign up with an affiliate OpenID provider."""
        sreg_req = sreg.SRegRequest(['nickname'], ['fullname', 'email'])
        href = sreg_req.toMessage().toURL(OPENID_PROVIDER_URL)

        message = """Get an OpenID at <a href=%s>%s</a>""" % (
            quoteattr(href), OPENID_PROVIDER_NAME)
        self.render(message)

    def renderSREG(self, sreg_data):
        if not sreg_data:
            self.wfile.write(
                '<div class="alert">No registration data was returned</div>')
        else:
            sreg_list = sreg_data.items()
            sreg_list.sort()
            self.wfile.write(
                '<h2>Registration Data</h2>'
                '<table class="sreg">'
                '<thead><tr><th>Field</th><th>Value</th></tr></thead>'
                '<tbody>')

            odd = ' class="odd"'
            for k, v in sreg_list:
                field_name = sreg.data_fields.get(k, k)
                value = cgi.escape(v.encode('UTF-8'))
                self.wfile.write(
                    '<tr%s><td>%s</td><td>%s</td></tr>' % (odd, field_name, value))
                if odd:
                    odd = ''
                else:
                    odd = ' class="odd"'

            self.wfile.write('</tbody></table>')

    def renderPAPE(self, pape_data):
        if not pape_data:
            self.wfile.write(
                '<div class="alert">No PAPE data was returned</div>')
        else:
            self.wfile.write('<div class="alert">Effective Auth Policies<ul>')

            for policy_uri in pape_data.auth_policies:
                self.wfile.write('<li><tt>%s</tt></li>' % (cgi.escape(policy_uri),))

            if not pape_data.auth_policies:
                self.wfile.write('<li>No policies were applied.</li>')

            self.wfile.write('</ul></div>')

    def buildURL(self, action, **query):
        """Build a URL relative to the server base_url, with the given
        query parameters added."""
        base = urlparse.urljoin(self.server.base_url, action)
        return appendArgs(base, query)

    def notFound(self):
        """Render a page with a 404 return code and a message."""
        fmt = 'The path <q>%s</q> was not understood by this server.'
        msg = fmt % (self.path,)
        openid_url = self.query.get('openid_identifier')
        self.render(msg, 'error', openid_url, status=404)

    def render(self, message=None, css_class='alert', form_contents=None,
               status=200, title="Python OpenID Consumer Example",
               sreg_data=None, pape_data=None):
        """Render a page."""
        self.send_response(status)
        self.pageHeader(title)
        if message:
            self.wfile.write("<div class='%s'>" % (css_class,))
            self.wfile.write(message)
            self.wfile.write("</div>")

        if sreg_data is not None:
            self.renderSREG(sreg_data)

        if pape_data is not None:
            self.renderPAPE(pape_data)

        self.pageFooter(form_contents)

    def pageHeader(self, title):
        """Render the page header"""
        self.setSessionCookie()
        self.send_header("Content-type","text/html; charset=UTF-8")
        self.wfile.write('''\
<html>
  <head><title>%s</title></head>
  <style type="text/css">
      * {
        font-family: verdana,sans-serif;
      }
      body {
        width: 50em;
        margin: 1em;
      }
      div {
        padding: .5em;
      }
      tr.odd td {
        background-color: #dddddd;
      }
      table.sreg {
        border: 1px solid black;
        border-collapse: collapse;
      }
      table.sreg th {
        border-bottom: 1px solid black;
      }
      table.sreg td, table.sreg th {
        padding: 0.5em;
        text-align: left;
      }
      table {
        margin: 0;
        padding: 0;
      }
      .alert {
        border: 1px solid #e7dc2b;
        background: #fff888;
      }
      .error {
        border: 1px solid #ff0000;
        background: #ffaaaa;
      }
      #verify-form {
        border: 1px solid #777777;
        background: #dddddd;
        margin-top: 1em;
        padding-bottom: 0em;
      }
  </style>
  <body>
    <h1>%s</h1>
    <p>
      This example consumer uses the <a href=
      "http://github.com/openid/python-openid" >Python
      OpenID</a> library. It just verifies that the identifier that you enter
      is your identifier.
    </p>
''' % (title, title))

    def pageFooter(self, form_contents):
        """Render the page footer"""
        if not form_contents:
            form_contents = ''

        self.wfile.write('''\
    <div id="verify-form">
      <form method="get" accept-charset="UTF-8" action=%s>
        Identifier:
        <input type="text" name="openid_identifier" value=%s />
        <input type="submit" value="Verify" /><br />
        <input type="checkbox" name="immediate" id="immediate" /><label for="immediate">Use immediate mode</label>
        <input type="checkbox" name="use_sreg" id="use_sreg" /><label for="use_sreg">Request registration data</label>
        <input type="checkbox" name="use_pape" id="use_pape" /><label for="use_pape">Request phishing-resistent auth policy (PAPE)</label>
        <input type="checkbox" name="use_stateless" id="use_stateless" /><label for="use_stateless">Use stateless mode</label>
      </form>
    </div>
  </body>
</html>
''' % (quoteattr(self.buildURL('verify')), quoteattr(form_contents)))

    response_code={}
    
    def send_response(self,v):
#        self.wfile.write("%s\n"%str(v))
        self.send_header("Status",str(v))
        
    def send_header(self,a,b):
#        self.wfile.write("%s: %s\n"%(a,b))
        self.response_code[a]=b

    def end_headers(self):
        pass
        
    def writeUserHeader(self):
        if self.user is None:
            t1970 = time.gmtime(0)
            expires = time.strftime(
                'Expires=%a, %d-%b-%y %H:%M:%S GMT', t1970)
            self.send_header('Set-Cookie', 'user=;%s' % expires)
        else:
            self.send_header('Set-Cookie', 'user=%s' % self.user)

#def main(host, port, data_path, weak_ssl=False):
#    # Instantiate OpenID consumer store and OpenID consumer.  If you
#    # were connecting to a database, you would create the database
#    # connection and instantiate an appropriate store here.
#    if data_path:
#        store = filestore.FileOpenIDStore(data_path)
#    else:
#        store = memstore.MemoryStore()
#
#    if weak_ssl:
#        setDefaultFetcher(Urllib2Fetcher())
#
#    addr = (host, port)
#    server = OpenIDHTTPServer(store, addr, OpenIDRequestHandler)
#
#    print 'Server running at:'
#    print server.base_url
#    server.serve_forever()
#
#if __name__ == '__main__':
#    host = 'localhost'
#    port = 8001
#    weak_ssl = False
#
#    try:
#        import optparse
#    except ImportError:
#        pass # Use defaults (for Python 2.2)
#    else:
#        parser = optparse.OptionParser('Usage:\n %prog [options]')
#        parser.add_option(
#            '-d', '--data-path', dest='data_path',
#            help='Data directory for storing OpenID consumer state. '
#            'Setting this option implies using a "FileStore."')
#        parser.add_option(
#            '-p', '--port', dest='port', type='int', default=port,
#            help='Port on which to listen for HTTP requests. '
#            'Defaults to port %default.')
#        parser.add_option(
#            '-s', '--host', dest='host', default=host,
#            help='Host on which to listen for HTTP requests. '
#            'Also used for generating URLs. Defaults to %default.')
#        parser.add_option(
#            '-w', '--weakssl', dest='weakssl', default=False,
#            action='store_true', help='Skip ssl cert verification')
#
#        options, args = parser.parse_args()
#        if args:
#            parser.error('Expected no arguments. Got %r' % args)
#
#        host = options.host
#        port = options.port
#        data_path = options.data_path
#        weak_ssl = options.weakssl
#
#    main(host, port, data_path, weak_ssl)

#form=cgi.FieldStorage()
#if not form.has_key("action"):
#    action=""
#else:
#    action=form["action"]

sessions=None
if os.path.exists(session_file):
    try:
        f=open(session_file,'r')
        sessions=pickle.load(f)
        f.close()
        f=None
    except:
        pass

if sessions==None:
    sessions={}

fakeheaders=FakeHeaders()
fakeheaders.set_environ(os.environ)

openidrequesthandler = OpenIDRequestHandler()
openidrequesthandler.server.sessions=sessions
openidrequesthandler.headers=fakeheaders
if "REQUEST_URI" in os.environ:
    openidrequesthandler.path=os.environ["REQUEST_URI"][len(uri_prefix):]
else:
    openidrequesthandler.path="/"
#openidrequesthandler.path="/verify?openid_identifier=http%3A%2F%2Fblog.luzi82.com%2F"
if(openidrequesthandler.path=="/consumer.py"):
    openidrequesthandler.path="/"
#openidrequesthandler.path="/~luzi82/HiSocial/test/consumer.py"
#openidrequesthandler.path="/~luzi82/HiSocial/test/consumer.py?action=verify"
openidrequesthandler.do_GET()
for k, v in openidrequesthandler.response_code.iteritems():
    sys.stdout.write("%s: %s\n"%(k,v))
sys.stdout.write("\n")
sys.stdout.write(openidrequesthandler.wfile.getvalue())

f=open(session_file,"w")
pickle.dump(openidrequesthandler.server.sessions,f)
f.flush()
f.close()
f=None

sys.stdout.write("<br/>\n")
sys.stdout.write("<br/>\n")
sys.stdout.write(openidrequesthandler.path)
sys.stdout.write("<br/>\n")
sys.stdout.write("<br/>\n")
sys.stdout.write(openidrequesthandler.my_path)
sys.stdout.write("<br/>\n")
sys.stdout.write("<br/>\n")
for k, v in openidrequesthandler.query.iteritems():
    sys.stdout.write("%s: %s<br/>\n"%(k,v))
sys.stdout.write("<br/>\n")
sys.stdout.write("<br/>\n")
for k, v in fakeheaders.environ.iteritems():
    sys.stdout.write("%s: %s<br/>"%(k,v))
sys.stdout.write("\n")