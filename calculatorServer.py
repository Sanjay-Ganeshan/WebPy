import WebPyCreator

def main():
    def add(x, y):
        #return {"result": x+y}
        a = WebPyServer.DynamicObject()
        a.result = x+y
        return a
    def subtract(x, y):
        #return {"difference": x-y, "positiveDifference": abs(x-y)}
        return x-y
    
    server = WebPyCreator.createServer([add,subtract])
    server.start()
    #server

if __name__ == "__main__":
    main()
