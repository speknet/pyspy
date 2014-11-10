if __name__ == '__main__':
    import socket
    import threading
    import Queue
    import time
    import win32gui, win32ui, win32con, win32api, Image, time, base64, socket
    import hashlib
    import sys

    def rightclickmouse(x,y):
        print "Right click here: "+str(x),str(y)
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

    def clickmouse(x,y):
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    def doscreenshot():
        hwin = win32gui.GetDesktopWindow()
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
        bmp.SaveBitmapFile(memdc, "bitmap.bmp")
        im = Image.open("bitmap.bmp")
        win32gui.DeleteObject(bmp.GetHandle())
        memdc.DeleteDC()
        srcdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        im.save("screenshot.jpg","JPEG",quality=30)
        with open("screenshot.jpg","rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string + '@'
        return encoded_string

    def mouseChannel():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.56.1', 4444))
        s.send("MOUSETRANSFER")
        while True:
            incomingData = s.recv(1024)
            if '@' in incomingData:
                coord = incomingData[:incomingData.find('@')]
                print incomingData
                xy = coord.split(',')
                if(xy[2]=='1'):
                    clickmouse(int(xy[0]),int(xy[1]))
                elif(xy[2]=='2'):
                    rightclickmouse(int(xy[0]),int(xy[1]))
                else:
                    print 'Mouse action error: '+incomingData

    def keyChannel():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.56.1', 4444))
        s.send("KEYTRANSFER")
        while True:
            incomingData = s.recv(1024)
            if incomingData != '':
                print incomingData
            s.send("HeartBeat")

    def streamChannel():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.56.1', 4444))
        s.send("SCREENTRANSFER")
        while True:
            x = doscreenshot()
            s.send(x)
            time.sleep(0.1)

    threads = []
    #keyThread = threading.Thread(target=keyChannel)
    #keyThread.setDaemon(True)
    #threads.append(keyThread)
    #keyThread.start()
    
    mouseThread = threading.Thread(target=mouseChannel)
    mouseThread.setDaemon(True)
    threads.append(mouseThread)
    mouseThread.start()
    
    streamThread = threading.Thread(target=streamChannel)
    streamThread.setDaemon(True)
    threads.append(streamThread)
    streamThread.start()
    #keyThread.join()
    mouseThread.join()
    streamThread.join()
