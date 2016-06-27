import time
import BaseHTTPServer
import json

def prettyPrint(obj):
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

def getArgs(fn):
    return list(fn.__code__.co_varnames)

class Evaluator():
    allFunctions = {}
    @staticmethod
    def setUp(newFunctions = {}):
        Evaluator.allFunctions = newFunctions
    @staticmethod
    def addFunction(httpCall, path, funcToExecute):
        if not(httpCall in Evaluator.allFunctions.keys()):
            Evaluator.allFunctions[httpCall] = {}
        Evaluator.allFunctions[httpCall][path] = (getArgs(funcToExecute), funcToExecute)
        
    @staticmethod
    def evaluate(httpCall, path, inputData):
        inputsToFind, funcToExecute = Evaluator.allFunctions[httpCall][path]
        allInputData = {} #only good data
        for eachInput in inputsToFind:
            print eachInput
            if eachInput in inputData.keys():
                allInputData[eachInput] = inputData[eachInput]
            else:
                return False, {"Error": eachInput + " is a required parameter"}
        return True, funcToExecute(**allInputData)

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
        worked,outputData = Evaluator.evaluate("POST", self.path, objectIn)
        if(worked):
            self.wfile.write(prettyPrint(outputData))
        else:
            self.wfile.write(prettyPrint(outputData))
        

def initServer():
    def add(a,b):
        return {"sum": a+b}
    def subtract(c,d):
        return {"difference": c-d, "positiveDifference": abs(c-d)}
    def multiply(a,b):
        return {"product": a * b }
    def divide(a,b):
        return {"quotient": float(a) / b, "reciprocal": float(b) / a}
    Evaluator.setUp()
    Evaluator.addFunction("POST","/api/add",add)
    Evaluator.addFunction("POST","/api/subtract",subtract)
    Evaluator.addFunction("POST","/api/multiply",multiply)
    Evaluator.addFunction("POST","/api/divide",divide)


def main(HOST_NAME, PORT_NUMBER):
    initServer()
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

if __name__ == "__main__":
    main("localhost",1337)