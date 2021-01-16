#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        split_data = self.data.split()
        
        req = split_data[0].decode('utf-8')
        requested_res = split_data[1].decode('utf-8')

        if req == "GET":
            self.request.sendall(bytearray('HTTP/1.1 200 OK\n', 'utf-8'))

            if requested_res == "/":
                requested_res = "/index.html"

            if requested_res.endswith("html"):
                self.request.sendall(bytearray('Content-Type: text/html\n\n', 'utf-8'))
            elif requested_res.endswith("css"):
                self.request.sendall(bytearray('Content-Type: text/css\n\n', 'utf-8'))

            f = open("www" + requested_res)
            self.request.sendall(f.read().encode('utf-8'))


        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
