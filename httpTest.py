import time
import BaseHTTPServer


import json

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 13377 # Maybe set this to 9000.

def add(objectIn):
    return objectIn['param1'] + objectIn['param2']

def subtract(objectIn):
    return objectIn['param1'] - objectIn['param2']

functions = {
    "add":add,
    "subtract":subtract,
}

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write("<html><head><title>Title goes here.</title></head>")
        self.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar",
        # then self.path equals "/foo/bar".
        if self.path == "/foo":
            self.wfile.write("<p>You accessed foo </p>")
        if self.path == "/foo/bar":
            self.wfile.write("<p>You accessed foo bar </p>")
        self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        self.wfile.write("</body></html>")

    def do_POST(self):
        """Respond to a POST request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
    
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)

        objectIn = json.loads(content)
        
        print functions[objectIn['function']](objectIn)




#on Startup
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)




