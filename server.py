# Source - https://stackoverflow.com/a/21957017
# Posted by poke, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-01, License - CC BY-SA 4.0

#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        if self.path.endswith('.pbf'):
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Type', 'application/x-protobuf')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
