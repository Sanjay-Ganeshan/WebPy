import WebPyServer

def initServer(evaluator):
    def add(a,b):
        return {"sum": a+b}
    def subtract(c,d):
        return {"difference": c-d, "positiveDifference": abs(c-d)}
    def multiply(a,b):
        return {"product": a * b }
    def divide(a,b):
        return {"quotient": float(a) / b, "reciprocal": float(b) / a}
    evaluator.setUp()
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/add",add))
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/subtract",subtract))
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/multiply",multiply))
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/divide",divide))

def main():
    myServer = WebPyServer.Server("localhost",1337,initServer)
    myServer.start()


if __name__ == "__main__":
    main()