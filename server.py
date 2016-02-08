# Basics of the code is taken from
# http://www.kellbot.com/2010/02/tutorial-writing-a-tcp-server-in-python/
# http://www.bogotobogo.com/python/python_network_programming_server_client.php


import socket as sc      #import the socket library
import time
from datetime import datetime
import generate_sine as gs 
import errno

reload(gs)
 
# Define a class containing the properties of a sine wave
class profilestructure:
	def __init__(self):
		self.amp   	= 0 # max amplitude
		self.freq       = 0 	# frequency
		self.ext        = False	# extension with zeros
		self.sampling   = 0 	# sampling frequency of the signal
		self.t_final 	= 0 	# duration of the wave [sec]

# ----------------

comm_freq  = 125        # communication frequency [Hz]


# Sine wave
# ------------
profile = profilestructure()
profile.amp     = 100   # max movement will be 100 [mm] as there is a division by 10 in KL code
profile.freq 	= 0.5   # freq values = {0.1, 0.2, 0.5, 1, 1.5, 2, 2.5, 3}
profile.ext 	= True
profile.sampling= comm_freq
profile.t_final = 2

sine_wave,t = gs.gen_profile_sine(profile)

# Scale the sine wave

scale_factor = 1

sine_wave = sine_wave*scale_factor;


# Message definition
#-------------------
# message: #2 X Y Z MAX_X_INC MAX_Y_INC MAX_Z_INC
# message: #+1234-1234+1234+1234+1234+1234

scale_factor_max_inc = 1        # allowed max absolute path change per offset change

CONST_STR  = 4          # length of the string

msg_header = '#2'
msg = []

x = sine_wave

for i in sine_wave:

        # Integer and rounded sine wave
        sine_rounded = int(round(i))

        msg_tmp = str(sine_rounded)                     # Turn to string
        msg_tmp = msg_tmp.replace('-','')               # Remove the negative signs
        msg_tmp = msg_tmp.rjust(CONST_STR, '0')         # Add extra zeros on the left side: 0123

        # add the sign to the string signal
        if sine_rounded >= 0:
                msg_tmp = "+" + msg_tmp
        else:
                msg_tmp = "-" + msg_tmp

        # Integer and rounded sine wave
        max_inc_rounded = abs(int(round(i*scale_factor_max_inc)))
        msg_max_inc = str(max_inc_rounded)
        msg_max_inc = msg_max_inc.rjust(CONST_STR, '0') 
        msg.append(msg_header + msg_tmp + "+0000+0000+" + msg_max_inc + "+0000+0000" )

#msg = ['#+0100-0000+0000+0500+0000+0000']
# The sent data is 10* [mm]
# +0100 is interpreted as 10 mm

# Server, connection
# -------------------
HOST = '192.168.0.10'  # we are the host
PORT = 2002 # arbitrary port not currently in use
ADDR = (HOST,PORT)    	# make a tuple for the address
BUFSIZE = 64    		# reasonably sized buffer for data

# create a new socket object (serv)
# & setup socket to listen for incoming connections
serv = sc.socket( sc.AF_INET,sc.SOCK_STREAM)    

print 'Socket is made!'
#
ADDR = ( sc.gethostname(), PORT)

# bind the socket to the address
serv.bind((ADDR))    #the double parens are to create a tuple with one element
#serv.bind((sc.gethostname(), PORT))
serv.listen(5)       #5 is the maximum number of queued connections we'll allow


print 'Listening for incoming connections...'

conn,addr = serv.accept() #accept the connection
print 'Connection from this address: ', addr


# Data exchange & writing the data to a file
# --------------------------------

raw_input("Press Enter to start the data transfer...")

# communication time for each message
comm_time  = 1.0/comm_freq

# Getting ready for the main data loop

file_data = []
while True:
        try:
                for i in msg:
                        clock_before_send = datetime.now()

                        conn.send(i)
                        
                        timestamp_before_send = clock_before_send.hour*3600.0 + clock_before_send.minute*60.0 + clock_before_send.second + clock_before_send.microsecond*1e-6 
                        clock_before_receive = datetime.now()
                        
                        data = conn.recv(BUFSIZE)

                        #print msg, data

                        timestamp_before_receive = clock_before_receive.hour*3600.0 + clock_before_receive.minute*60.0 + clock_before_receive.second + clock_before_receive.microsecond*1e-6 

                        clock_after_operation = datetime.now()
                        timestamp_after_operation = clock_after_operation.hour*3600.0 + clock_after_operation.minute*60.0 + clock_after_operation.second + clock_after_operation.microsecond*1e-6 

                        file_data.append(str(timestamp_before_send) + " " + str(timestamp_before_receive) + " " + str(timestamp_after_operation) + " " + " " + i + " " + data + "\n" )

                        comm_time_curr_msg = timestamp_after_operation-timestamp_before_send

                        # raw_input("Sent & Received, Press ENTER.")
                        if comm_time_curr_msg <= comm_time:
                                time.sleep(comm_time-comm_time_curr_msg)
        except sc.error, e:
                if isinstance(e.args, tuple):
                        print "ERR no %d" % e[0]
                        if e[0] == errno.EPIPE:
                                # remote peer disconnected
                                print "Detected remote disconnect"
                                conn.close()
                                break
                        else:
                                # determine and handle different error
                                print "Another error, don't know which one yet"
                                conn.close()
                                break
                                pass
                else:
                        print "socket error ", e


                        conn.close()
                        break
        except IOError, e:

                # Hmmm, Can IOError actually be raised by the socket module?
                print "Got IOError: ", e

                conn.close()
                break

conn.close()
serv.close()

f = open('report.txt', 'w')

for i in file_data:
        f.write(i)

f.close()

# --------------------------------
# --------------------------------

