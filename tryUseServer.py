import WebPyServer

def initServer(evaluator):
    def add(a,b):
        sum = a + b
        return {"sum": sum}
    def subtract(globalState,c,d):
        return {"difference": c-d, "positiveDifference": abs(c-d)}
    def multiply(globalState,a,b):
        return {"product": a * b }
    def divide(globalState,a,b):
        return {"quotient": float(a) / b, "reciprocal": float(b) / a}
    def doStuff(globalState):
        numToReturn = 0
        try:
            numToReturn = globalState.myNumber
            globalState.myNumber += 1
        except Exception,e:
            globalState.myNumber = numToReturn
        return {"RetVal": numToReturn}
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/add",add))
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/subtract",subtract))
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/multiply",multiply))
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/divide",divide))
    evaluator.addFunction(WebPyServer.HttpEndpoint("POST","/api/doStuff",doStuff))

def main():
    myServer = WebPyServer.Server("localhost",1337,initServer)
    myServer.start()


if __name__ == "__main__":
    main()