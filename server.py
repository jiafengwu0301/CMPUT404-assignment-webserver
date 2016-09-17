# coding: utf-8

import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Jiafeng Wu
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



class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "Got a request of: %s\n" % self.data

        # split the request infomation into a list
    	requestList = self.data.split()

        # get the method
    	requestMethod = requestList[0]
        # get the path
    	requestUrl = requestList[1]
        # get the protocol
        requestProtocol = requestList[2]

        # get the absolute path of folder www
        root_path = os.path.abspath("www")

        # security check, parent of current directory
    	if '../' in requestUrl:
            self.request.sendall(str(requestProtocol)+" 404 Not Found\r\n\r\n")
            self.request.sendall("404 ERROR - PAGE NOT FOUND")

        # check path and get the absolute path of files
        else:
            #init the absolute path
            abs_path = ""

            #if the "/" at the end, update the absolute path by adding root_path,requestUrl and index.html
            if requestUrl[-1] == '/':
                abs_path = root_path + requestUrl + "/index.html"

            # else, update the absolute path by adding root path and the requestUrl
            else:
                abs_path = root_path + requestUrl

            # if the requestMethod is GET, call function getMethod
            if requestMethod.upper() == "GET":
                self.getMethod(abs_path,requestProtocol)


    def getMethod(self,abs_path,requestProtocol):
        # if can open the absolute path, open file and send all the information
    	try:
            # open the file by the absolut path
    	    f = open(abs_path)
            # read the file
    	    f_text = f.read()

            # determine the mimetype of file
            mime = ""
            if abs_path.lower().endswith(".html"):
                mime = "text/html"

            elif abs_path.lower().endswith(".css"):
                mime = "text/css"

            #send header
            self.request.sendall(str(requestProtocol)+" 200 OK\r\n")
            self.request.sendall("Content-Type: "+str(mime)+"\r\n")
            self.request.sendall("Content-Length: "+str(len(f_text))+"; charset = utf-8\r\n")
    	    self.request.sendall('Connection: close' + "\r\n\r\n")

            #send data
    	    self.request.sendall(f_text + "\r\n")

            # close the file
            f.close()

        # if the absolute path is not exist, throw the 404 error
    	except:
    	    self.request.sendall(str(requestProtocol)+" 404 Not Found\r\n\r\n")
    	    self.request.sendall("404 ERROR - PAGE NOT FOUND")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
