#!/bin/env python3
DEFAULT_HTTP_INTERFACE = ''
DEFAULT_HTTP_PORT = 80

import sys
from http import server # Python 3

def item_default(o,i=0, default=None):
    try:
        return o[i]
    except:
    	return default

def int_default(s, default=None):
    try:
        return int(s)
    except:
    	return default

def parseUrl(url = '', default_host=DEFAULT_HTTP_INTERFACE, default_port=DEFAULT_HTTP_PORT):
    try:
      pasedUrl = url.split(':',1)
      host = item_default(pasedUrl, 0) or default_host
      port = int_default(item_default(pasedUrl, 1)) or default_port
      return (host, port)
    except:
      return (default_host, default_port)
  

class ThisHTTPRequestHandler(server.SimpleHTTPRequestHandler):

    def _return(self, status, content = '', headers = {}):
        bytes = content.encode()
        self.send_response(status)
        for k,v in headers.items():
        	self.send_header(k,v)
        self.send_header('Content-Length',len(bytes))
        self.end_headers()
        self.wfile.write(bytes)

    def do_GET(self):
        try:
            key = self.headers[HEADER_KEY]
            value = "TODO"
            if value == None:
                return self._return(404)
            return self._return(200,headers={HEADER_VALUE:value})
        except:
            return self._return(500)

    def do_POST(self):
        try:
            key = self.headers[HEADER_KEY]
            value = self.headers[HEADER_VALUE] or DEFAULT_VALUE
            time = int_default(self.headers[HEADER_TIME]) or DEFAULT_TIME
            if not key:
                return self._return(400)
            return self._return(200)
        except:
            return self._return(500)

if __name__ == '__main__':
    if '--help' == item_default(sys.argv,1):
        print(f'Use: {sys.argv[0]} [<http_interface>:<http_port>]')
        print(f'Default arguments: {DEFAULT_HTTP_INTERFACE}:{DEFAULT_HTTP_PORT}')
        sys.exit()

    thisServerUrl=item_default(sys.argv,1,f'{DEFAULT_HTTP_INTERFACE}:{DEFAULT_HTTP_PORT}')
    httpd = server.HTTPServer(parseUrl(thisServerUrl), ThisHTTPRequestHandler)
    httpd.serve_forever()
