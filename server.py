import json
from pprint import pprint
import bike
import rpyc
import thread
import Tkinter as tk
from rpyc.utils.server import ThreadedServer



PORT = 8000
PATH = 'bikes.txt'
LOGIN_PIC_PATH = 'login.ppm'

class ServerService(rpyc.Service):
    path = PATH
    """docstring for Server."""
    def __init__(self, arg = None):
        #print 'created server'
        pass

    def loadBikes(self):
        try:
            bikes = json.load(open(self.path))
        except:
            bikes = []
        return bikes

    def exposed_getAvailable(self):
        #print 'available called'
        bikes = self.loadBikes()
        return [bike for bike in bikes if bike['status'] == 'available']

    def listBikes(self):
        bikes = self.loadBikes()
        for bik in bikes:
            bike.printBike(bik)

    def addBike(self, bike):
        bikes = self.loadBikes()
        bikes.append(bike.getJson())
        json.dump(bikes, open(self.path, 'w'))

    def removeBike(self, id):
        bikes = self.loadBikes()
        bikes = [bike for bike in bikes if bike['id'] != id]
        json.dump(bikes, open(self.path, 'w'))

    def checkCode(self, bike, code):
        return code == code # TODO add code checking

    def exposed_handleBikeRequest(self, id, code, request):
        bikes = self.loadBikes()
        conditionState = 'available' if request == 'get' else 'unavailable'  if request == 'let' else None
        resultState =  'unavailable' if request == 'get' else 'available'  if request == 'let' else None
        if (conditionState is None or resultState is None):
            return 'unknown'
        for bike in bikes:
            if (bike['status'] == conditionState and bike['id'] == id and self.checkCode(bike, code)):
                bike['status'] = resultState
                json.dump(bikes, open(self.path, 'w'))
                return 'success'
        return 'fail'
        #  TODO update bike

def getUserRequest():
    return raw_input('what would you like to do? (add, remove, display, gui, exit) ')

def handleGui():
    startGui()

def handleAdd():
    id = input('bike id: ')
    status =  raw_input('bike status: ')
    location = bike.Location(input('bike location x: '), input('bike location y: '))
    server.addBike(bike.Bike(id, status, location))

def handleRemove():
    id = input('bike id: ')
    server.removeBike(id)

def handleDisplay():
    server.listBikes()

def handleExit():
    return 'exit'

def handleUnknown():
    print 'I wanna nothing'

def handleRequest(request):
    handlers = {
        'add' : lambda : handleAdd(),
        'remove' : lambda : handleRemove(),
        'display' : lambda : handleDisplay(),
        'gui': lambda : handleGui(),
        'exit' : lambda : handleExit()
    }

    return handlers.get(request, lambda : handleUnknown())()

server = ServerService()

def server_start():
    serverr = ThreadedServer(ServerService, port = PORT, protocol_config={"allow_public_attrs": True, "allow_all_attrs": True})
    serverr.start()

def handleGuiAdd():
    id = int(idEntry.get())
    status = statusEntry.get()
    x, y = locationEntry.get().split(',')
    location = bike.Location(float(x), float(y))
    server.addBike(bike.Bike(id, status, location))

def handleGuiRemove():
    id = int(idEntry.get())
    server.removeBike(id)

def handleGuiDisplay():
    pop =  tk.Tk()
    pop.title("All bikes")
    bikes = server.loadBikes()
    for bikk in bikes:
        label = tk.Label(pop,
                        compound = tk.CENTER,
                        text=json.dumps(bikk))
        label.pack()
    pop.mainloop()



def startGui():
    global idEntry
    global statusEntry
    global locationEntry
    root = tk.Tk()

    root.title("Server")
    # logo = tk.PhotoImage(file=LOGIN_PIC_PATH)
    # w = tk.Label(root,
    #          compound = tk.CENTER,
    #          text="""press start""",
    #          image=logo).pack(side="right")
    tk.Button(root, text='add', width=25, command=handleGuiAdd).grid(row = 0)
    tk.Button(root, text='remove', width=25, command=handleGuiRemove).grid(row = 1)
    tk.Button(root, text='display', width=25, command=handleGuiDisplay).grid(row = 2)

    tk.Label(root, text="id").grid(row=0, column = 1)
    tk.Label(root, text="status").grid(row=1, column = 1)
    tk.Label(root, text="x, y").grid(row = 2, column = 1)

    idEntry = tk.Entry(root)
    statusEntry = tk.Entry(root)
    locationEntry = tk.Entry(root)

    idEntry.grid(row=0, column = 2)
    statusEntry.grid(row=1, column = 2)
    locationEntry.grid(row = 2, column = 2)

    root.mainloop()
    return root

def main():
    print 'server started'
    thread.start_new_thread(server_start, ())
    result = ''
    while (result != 'exit'):
        result = handleRequest(getUserRequest())
    print 'server done'
if __name__ == '__main__':
    main()
