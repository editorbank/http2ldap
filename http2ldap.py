#!/bin/env python3

import json
import sys
from http import server
from urllib.parse import urlparse # Python 3
from get_args import get_args
from ldap_query import check_form

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

class ThisHTTPRequestHandler(server.SimpleHTTPRequestHandler):

    def _return(self, status, content = '', headers = {}):
        bytes = content.encode()
        self.send_response(status)
        for k,v in headers.items():
            self.send_header(k,v)
        self.send_header('Content-Length',len(bytes))
        self.end_headers()
        self.wfile.write(bytes)

    def _request(self, query_string):
        try:
            result = check_form(query_string, args.ldap_server, args.ldap_user, args.ldap_password, args.search_base, args.search_filter, args.attributes)
            entries = result.get("entries")
            if not entries or len(entries) != 1:
                return self._return(400, result.get("error","an empty record or more than one record was returned")+"\r\n")
            attributes = dict({"dn": entries[0]["dn"]})
            attributes.update({k:",".join(v) if type(v) is list else f"{v}" for k,v in entries[0]["attributes"].items()})
            return self._return(200, "OK\r\n", attributes)
        except Exception as err:
            return self._return(500, f"{err}\r\n")

    def do_GET(self):
        query_string = urlparse(self.path).query
        return self._request(query_string)

    def do_POST(self):
        query_string = urlparse(self.path).query
        query_body = self.rfile.read(int(self.headers['Content-Length'])).decode()
        return self._request(query_string + ('&' if query_string and query_body else '') + query_body)

if __name__ == '__main__':
    args = get_args()
    print( args )
    if args.test_query_string:
        print( check_form(args.test_query_string, args.ldap_server, args.ldap_user, args.ldap_password, args.search_base, args.search_filter, args.attributes) )
    else:
        try:
            httpd = server.HTTPServer((args.http_interface, args.http_port), ThisHTTPRequestHandler)
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            print("\nServer stopped.")
