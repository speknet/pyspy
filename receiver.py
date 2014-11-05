import socket
import sys
from threading import Thread
import PIL
from io import BytesIO
from cStringIO import StringIO
import base64
import hashlib
import ImageTk
import threading

from Tkinter import *


def start_server():
	HOST = '192.168.56.1'
	PORT = 4444
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((HOST, PORT))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	s.listen(10)
	print 'Socket now listening'
	while 1:
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		t = Thread(target=clientthread,args=(conn,))
		t.start()
	s.close()

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	lock = threading.Lock()
	End = '@'
	totaldata = ''
	while 1:
		data = conn.recv(1024)
		if End in data:
			totaldata+=data[:data.find(End)]
			jpegdata = StringIO(base64.b64decode(totaldata))
			readyframe = PIL.Image.open(jpegdata)
			newIMG = ImageTk.PhotoImage(readyframe)
			studFiles.set(newIMG)
			totaldata = ''
		else:
			totaldata+=data
		if not data:
			break

t = Thread(target=start_server).start()

def callback(*args):
	readyframe = studFiles.get()
	if readyframe != '':
		#img2 = PhotoImage(data=newIMG)
		#img2 = PhotoImage(image=newIMG)
		label.configure(image=readyframe)
		label.image = readyframe

app = Tk()
app.title("Example")

studFiles = StringVar()
studFiles.trace("w", callback)

# List of photoimages for each image
photo = PhotoImage(data=studFiles.get())
label = Label(image=photo)
label.pack()

app.mainloop()

