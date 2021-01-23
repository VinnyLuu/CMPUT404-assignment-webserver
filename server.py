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

    def get_data(self):
        self.data = self.request.recv(1024).strip().decode("utf-8")
        if self.data is None or len(self.data) == 0:
            return {}
            
        fields = self.data.split("\r\n")
        output = {"method" : fields[0].split()[0], "resource" : fields[0].split()[1]}
        fields = fields[1:] #ignore the GET / HTTP/1.1
        
        for field in fields:
            if not field:
                continue
            key,value = field.split(': ')
            output[key] = value
        return output


    def send_header(self, code, filename):
        status = "HTTP/1.1 " + str(code) + "\n"
        self.request.sendall(status.encode('utf-8'))
        if code >= 400:
            return

        if code >= 300:
            location = "Location: http://" + self.response_params["Host"] + filename + "\n\n"
            self.request.sendall(location.encode('utf-8'))
            return

        if filename.endswith("html"):
            self.request.sendall(bytearray('Content-Type: text/html\n\n', 'utf-8'))
        elif filename.endswith("css"):
            self.request.sendall(bytearray('Content-Type: text/css\n\n', 'utf-8'))
    

    def send_file(self, filename):
        try:
            code = 200
            if ".." in filename or "~" in filename:
               self.send_header(404, filename)
               return

            if filename.endswith("/"):
                filename += "index.html"

            f = open("www" + filename)
            self.send_header(code, filename)
            self.request.sendall(f.read().encode('utf-8'))

        except IsADirectoryError as e:
            filename += "/"
            code = 301
            self.send_header(code, filename)
            
        except FileNotFoundError as e:
            self.send_header(404, filename)
        

    def handle(self):
        self.response_params = self.get_data()
        if self.response_params is None or len(self.response_params) == 0:
            return

        if self.response_params["method"] == "GET":
            self.send_file(self.response_params["resource"])
        else:
            self.send_header(405, "")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
