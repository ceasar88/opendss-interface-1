import socket
import csv
import subprocess
from subprocess import Popen, PIPE

import os
#from win32com.client import Dispatch

def Main():
	#connect################################################################################################

        host = '127.0.0.1'
        port = 1887
        mySocket = socket.socket()
	#mySocket.settimeout(8)	#set timer change if need be...
        mySocket.connect((host,port))
	#mySocket.setblocking(0)
	#open csv  and send table to server######################################################################
       	with open('openDSS.CSV', 'rb') as csvfile:
		opendssCsv = csv.reader(csvfile, delimiter=' ')
		data = list(opendssCsv)
   		row_count = len(data)
	print(row_count)
	csvData = str(row_count)
	with open('openDSS.CSV', 'rb') as csvfile:
		opendssCsv = csv.reader(csvfile, delimiter=' ')
		for row in opendssCsv:
			message = ''.join(row)
			#print ('data from csv: ' +message)
			csvData = csvData + '\n' + message
        mySocket.send(csvData.encode())
	print("done reading csv, data sent: "+csvData)

	#create receive command from device server##################################################
	while mySocket.recv(255):	#loop is terminated by socket timer or otherwise use infinite loop
		data = mySocket.recv(255)
		if data:
			text_file = open("Output.txt", "w")
			text_file.write(data)
			text_file.close()
		#update(data)
		#check for csv file update and resend
	mySocket.close()
	
	#call c++ code if required #############################################################################
	#p = subprocess.Popen([r"/usr/bin/g++", "-Wall", "-o", "test", 'test.cpp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#p.communicate()
	#p = subprocess.Popen(["test.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#p.communicate()
	#result = p.stdout.readline().strip()
    	#print(result)

	#load openDSS com server ###############################################################################
	
def update(str):
	dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
       	print('loaded....')
	dssCircuit = dssObj.ActiveCircuit
	#dssBus = dssCircuit.ActiveBus
	dssBus = str.split(',')[0].split(':')[1]
	BusNode = str.split(',')[1].split(':')[1]
	#dssCircuit.Loads.Name = loadName.split('.')[1]
	#oldkvar = dssCircuit.Loads.kvar
	dssCircuit.Loads.kvar = float(str.split(',')[2].split(':')[1])
	print('updated....')
def test():
	Main()
	
if __name__ == '__main__':
    test()
