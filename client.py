import rpyc
import bike
import Tkinter as tk
from pprint import pprint
from pprint import pformat
import json
PORT = 8000
conn = rpyc.connect("localhost", PORT, config={"allow_all_attrs":True})

def getUserRequest():
    return raw_input('what would you like to do? (let, get, display, gui, exit) ')

def handleLet():
    id = input("bike id: ")
    return conn.root.handleBikeRequest(id, None, 'let')

def handleGet():
    id = input("bike id: ")
    return conn.root.handleBikeRequest(id, None, 'get')

def handleExit():
    return 'exit'

def handleUnknown():
    print 'I wanna nothing'

def guiMessage(message):
    pop =  tk.Tk()
    pop.title("File content")
    label = tk.Label(pop, text=message)
    label.pack()
    button = tk.Button(pop, text='OK', width=25, command=pop.destroy)
    button.pack()
    pop.mainloop()

def handleGuiGet():
    id = int(idEntry.get())
    result = conn.root.handleBikeRequest(id, None, 'get')
    guiMessage(result)

def handleGuiLet():
    id = int(idEntry.get())
    result = conn.root.handleBikeRequest(id, None, 'let')
    guiMessage(result)

def handleDisplay():
    bikes = conn.root.getAvailable()
    for bik in bikes:
        pprint (bik, indent=0)
        #bike.printBike(bik)

def handleGuiDisplay():
    pop = tk.Tk()
    pop.title("Available bikes")
    bikes = conn.root.getAvailable()
    for bikk in bikes:
        label = tk.Label(pop,
                        compound = tk.CENTER,
                        text=pformat(bikk))
        label.pack()
    pop.mainloop()

def handleGui():
    startGui()

def startGui():
    global idEntry

    root = tk.Tk()
    root.title("Server")
    # logo = tk.PhotoImage(file=LOGIN_PIC_PATH)
    # w = tk.Label(root,
    #          compound = tk.CENTER,
    #          text="""press start""",
    #          image=logo).pack(side="right")
    tk.Button(root, text='let', width=25, command=handleGuiLet).grid(row = 0)
    tk.Button(root, text='get', width=25, command=handleGuiGet).grid(row = 1)
    tk.Button(root, text='display', width=25, command=handleGuiDisplay).grid(row = 2)

    tk.Label(root, text="id").grid(row=0, column = 1)

    idEntry = tk.Entry(root)

    idEntry.grid(row=0, column = 2)

    root.mainloop()
    return root

def handleRequest(request):
    handlers = {
        'let' : lambda : handleLet(),
        'get' : lambda : handleGet(),
        'display' : lambda : handleDisplay(),
        'gui': lambda : handleGui(),
        'exit' : lambda : handleExit()
    }

    return handlers.get(request, lambda : handleUnknown())()



def main():
    print 'client'
    result = ''
    while (result != 'exit'):
        result = handleRequest(getUserRequest())
        print result
    print 'client done'

if __name__ == '__main__':
    main()
