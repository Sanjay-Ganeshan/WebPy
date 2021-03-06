import WebPyServer

def createServer(functions, hostname = "localhost", port = 8080):
    '''
    def add(x, y):
        #return {"result": x+y}
        a = WebPyServer.DynamicObject()
        a.result = x+y
        return a
    def subtract(x, y):
        #return {"difference": x-y, "positiveDifference": abs(x-y)}
        return x-y
    def initServer(evaluator):
        evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/add",add))
        evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/subtract",subtract))
    '''
    def initServer(evaluator):    
        for eachFunction in functions:
            evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/" + eachFunction.__name__,eachFunction))
        

    server = WebPyServer.Server(hostname,port,initServer)
    return server

