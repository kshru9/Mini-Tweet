import socket
import threading
from _thread import *

# # initialising lock
# main_lock = threading.Lock()

# def thread_func(connection, filename):
# """Function which sends data to connected client"""

# 	fd = open(filename, "rb")

# 	l = fd.read(64*1024)
# 	while(l):
# 		connection.send(l)
# 		l = fd.read(64*1024)
	
# 	connection.send(bytes("EOF", 'utf-8'))
# 	print('Done sending')
# 	main_lock.release()

def home_page(client_conn, username):

	while True:
		client_conn.send(
			bytes(
				"""
				Reply with:
				1: for login
				2: for creating account
				3: your profile
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if not response:
			continue

		if (response == "1"):
			login_page()
		el

# hostname and port number
host = "localhost"
port = 12345

# count for number of threads
thread_count = 0

# declaring socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

# listening for client
s.listen(5)

while True:
	# got the connection from client
	connection, addr = s.accept()

	connection.settimeout(100)

	# data = connection.recv(1024)

	# # if client do not send any data, close the connection and exit
	# if not data:
	# 	print("Bye")
	# 	connection.close()
	# 	break

	# filename = data.decode() + ".txt"
	
	# # for a single file requested, acquire the lock and create a new thread to send the file
	# main_lock.acquire()
	# print('connection from:', repr(addr))

	# thread_count+=1
	# print(thread_count)

	# # start new thread
	# start_new_thread(thread_func, (connection, filename, ))

# close the socket object
s.close()