##client.py
import socket as sc
#import msvcrt
import time 

HOST = '127.0.0.1'
PORT = 2002    #our port from before
ADDR = (HOST,PORT)
BUFSIZE = 32

cli = sc.socket( sc.AF_INET,sc.SOCK_STREAM)
cli.connect((sc.gethostname(),PORT))

print("Connected...\n")


while True:
#        if msvcrt.kbhit():
#                if ord(msvcrt.getch()) == 27:
#                        break
#        else:
        data = cli.recv(BUFSIZE)
        # print data
        time.sleep(0.005)
        cli.send(data)


cli.close()
