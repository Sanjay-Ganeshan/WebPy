import time
import BaseHTTPServer
import json

def prettyPrint(obj):
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

def getArgs(fn):
    return list(fn.__code__.co_varnames)

class HttpEndpoint:
    def __init__(self, httpCall, path, funcToExecute):
        self.httpCall = httpCall
        self.path = path
        self.funcToExecute = funcToExecute
        self.inputs = getArgs(self.funcToExecute)

class Evaluator:
    allFunctions = {}
    @staticmethod
    def setUp(newFunctions = {}):
        Evaluator.allFunctions = newFunctions
    @staticmethod
    def addFunction(endpoint):
        #endpoint is an HttpEndpoint
        if not(endpoint.httpCall in Evaluator.allFunctions.keys()):
            Evaluator.allFunctions[endpoint.httpCall] = {}
        Evaluator.allFunctions[endpoint.httpCall][endpoint.path] = endpoint
        
    @staticmethod
    def evaluate(httpCall, path, inputData):
        inputsToFind, funcToExecute = Evaluator.allFunctions[httpCall][path].inputs,Evaluator.allFunctions[httpCall][path].funcToExecute
        allInputData = {} #only good data
        for eachInput in inputsToFind:
            if eachInput in inputData.keys():
                allInputData[eachInput] = inputData[eachInput]
            else:
                return False, {"Error": eachInput + " is a required parameter"}
        return True, funcToExecute(**allInputData)

class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
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
        worked,outputData = Evaluator.evaluate("POST", self.path, objectIn)
        if(worked):
            self.wfile.write(prettyPrint(outputData))
        else:
            self.wfile.write(prettyPrint(outputData))

class Server:
    def __init__(self, HOST_NAME, PORT_NUMBER, initFunction):
        self.HOST_NAME = HOST_NAME
        self.PORT_NUMBER = PORT_NUMBER
        Evaluator.setUp()
        initFunction(Evaluator)
        self.generateServer()
    def generateServer(self):
        server_class = BaseHTTPServer.HTTPServer
        self.httpd = server_class((self.HOST_NAME, self.PORT_NUMBER), ServerHandler)
    def start(self):
        print time.asctime(), "Server Starts - %s:%s" % (self.HOST_NAME, self.PORT_NUMBER)
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        self.httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (self.HOST_NAME, self.PORT_NUMBER)

    def close(self):
        print "LOL NO"