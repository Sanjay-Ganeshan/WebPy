import WebPyCreator

def main():
    def add(x, y):
        #return {"result": x+y}
        a = x+y
        return {"answer": a}
    def subtract(x, y):
        #return {"difference": x-y, "positiveDifference": abs(x-y)}
        return ["difference", x-y]
    
    server = WebPyCreator.createServer([add,subtract])
    server.start()
    #server

if __name__ == "__main__":
    main()
