import threading
import SocketServer
import time
from Tkinter import *
import socket
import sys
import PIL
from io import BytesIO
from cStringIO import StringIO
import base64
import hashlib
import ImageTk

lock = threading.Lock()
waitkey = threading.Event()

sendClick = '0'
sendRightClick = '0'
sendKey = '0'

class pyspyRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.SCREENTRANSFER = False
        self.MOUSETRANSFER = False
        self.KEYTRANSFER = False
        cur_thread = threading.currentThread()
        selectChannel = self.request.recv(14)
        print cur_thread.getName()+" ->> "+ selectChannel
        if selectChannel == 'SCREENTRANSFER':
            print cur_thread.getName() + ' SCREEN'
            self.SCREENTRANSFER = True
        elif selectChannel == 'MOUSETRANSFER':
            print cur_thread.getName() + ' MOUSE'
            self.MOUSETRANSFER = True
        elif selectChannel == 'KEYTRANSFER':
            print cur_thread.getName() + ' KEYBOARD'
            self.KEYTRANSFER = True         
        
        if(self.SCREENTRANSFER == True):
            totaldata = ''
            endofdata = '@'
            while True:
                stream = self.request.recv(1024)
                if(endofdata in stream):
                    totaldata+=stream[:stream.find(endofdata)]
                    jpegdata = StringIO(base64.b64decode(totaldata))
                    readyframe = PIL.Image.open(jpegdata)
                    newIMG = ImageTk.PhotoImage(readyframe)
                    streamvar.set(newIMG)
                    totaldata = ''
                else:
                    totaldata+=stream
        if(self.MOUSETRANSFER == True):
            global sendClick
            global sendRightClick
            while True:
                time.sleep(0.1)
                if (sendClick != '0'):
                    self.request.send(sendClick)
                    sendClick = '0'
                elif (sendRightClick != '0'):
                    self.request.send(sendRightClick)
                    sendRightClick = '0'
        if(self.KEYTRANSFER == True):
            global sendKey
            while True:
                waitkey.wait()
                if(sendKey != '0'):
                    print 'Sending Key: '+sendKey
                    self.request.send(sendKey)
                    with lock:
                        sendKey = '0'
                
        
        return

class pyspyNetworkServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def clicked(event):
    global sendClick
    sendClick = str(event.x)+','+str(event.y)+',1@'

def rightclicked(event):
    global sendRightClick
    sendRightClick = str(event.x)+','+str(event.y)+',2@'

def callback(*args):
    readyframe = streamvar.get()
    if readyframe != '':
        label.configure(image=readyframe)
        label.image = readyframe

def keypress(event):
    global sendKey
    with lock:
        sendKey = repr(event.char)+'!+!'.ljust(10, '#')
        waitkey.set()
        waitkey.clear()


address = ('192.168.56.1', 4444) # let the kernel give us a port
server = pyspyNetworkServer(address, pyspyRequestHandler)

t = threading.Thread(target=server.serve_forever)
t.setDaemon(True) # don't hang on exit
t.start()
print 'Server loop running in thread:', t.getName()

app = Tk()
app.title("Example")
#app.bind('<Motion>', motion)
app.bind("<Button-1>", clicked)
app.bind("<Button-3>", rightclicked)
app.bind("<Key>", keypress)
streamvar = StringVar()
streamvar.trace("w", callback)

# List of photoimages for each image
photo = PhotoImage(data=streamvar.get())
label = Label(image=photo)
label.pack()

app.mainloop()
