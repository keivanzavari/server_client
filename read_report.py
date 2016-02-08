#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports
import numpy as np
import matplotlib.pyplot as plt

# Give the name of the files
data_file = 'report.txt'

#readFile = open(data_file)
#lines = readFile.readlines()
#readFile.close()

# Read the file in a list
with open(data_file,'r') as myfile:
	data_list =[rows.split() for rows in myfile]

#headers = data_list[0]
#no_columns = len(headers)
no_rows = len(data_list)
no_cols = len(data_list[0])


timestamp_before_send = []
timestamp_after_operation = []
sent_str = []
recv_str = []

for i in range(0,no_rows):
        timestamp_before_send.append(float(data_list[i][0]))
        timestamp_after_operation.append(float(data_list[i][2]))
        sent_str.append(data_list[i][3])
        recv_str.append(data_list[i][4])

        sent_x = int(sent_str[2:7])
        recv_x = int(recv_str[2:7])

        sent_x_inc
       

for i in sent_str:


## Change the space to underscore, remove nextline character
#for row_i in lines:
#        row_i = row_i.replace(" ","_")
#        row_i = row_i.replace("\n","")
#        data_list.append(row_i) 

## Initialize the data
#print 'WARNING!\nTimeStamp is considered as the first column of the data file.'
##data_list = data_list.remove(data_list[0])            # Remove the first row
#data_array = np.asarray(data_list)               # Set to an array
#data_array = np.vstack(data_array)
#data_array_t = data_array.transpose()

#time_stamp = data_array_t[0][0:3]
#measurements = data_array_t[1:no_columns]


### Plot the data
##plt.figure()
###plt.subplot(211)
#plt.plot(time_stamp,measurements[-1])
#plt.grid(True)
#plt.ylabel('sensor small spline')
#plt.show()

#plt.subplot(212)
#plt.plot(time_large,sensor_large)
##plt.axis([0, Tfinal, Lm-0.05, LM+0.05])
#plt.grid(True)
#plt.ylabel('sensor lage spline')
 

