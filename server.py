import socket
import threading
# from _thread import *
import pickle
from utils import *
from database import *

def profile_page(client_conn, database, username):
	while True:
		details = db_get_user_details(database, username)
		
		followers = db_get_user_followers(database, username)
		
		profile_message = """Your Profile details"""
		client_conn.send(
			bytes(
				"""Your Profile details:
					Username: 
				""" + username
				"""Followers: """ + 
				
			, 'utf-8')
		)
		
def user_feed_page(client_conn, database, username):

def user_followers_page(client_conn, database, username):
	while True:
		followers = db_get_user_followers(database, username)

		client_conn.send(
			bytes(
				"""Your Followers are:
				""" + followers
			, 'utf-8')
		)

def user_followings_page(client_conn, database, username):
	while True:
		followers = db_get_user_following(database, username)

		client_conn.send(
			bytes(
				"""People whom you follow are:
				""" + followers
			, 'utf-8')
		)

def user_tweets_page(client_conn, database, username):
	while True:
		tweets = db_get_user_tweets(database, username)

		client_conn.send(
			bytes(
				"""Your Tweets are:
				""" + tweets
			, 'utf-8')
		)

def login_page(client_conn, database):
	"""A function to send login page to client"""

	while True:
		client_conn.send(
			bytes(
				"""Enter your username and password:"""
			, 'utf-8')
		)

		username = client_conn.recv(1024).decode()
		password = client_conn.recv(1024).decode()

		auth = login_auth(database, username, password)
		if (auth):
			client_conn.send(
				bytes(
					"""Login Successful!
						Where you want to see next?
						Reply with:
						1: Profile page
						2: Your feed
						3: Your followers
						4: Your followings
						5: Your tweets
						6: Exit
					"""
				, 'utf-8')
			)
			
			response = client_conn.recv(1024).decode()

			if (response == "1"):
				profile_page(client_conn, database)
			elif (response == "2"):
				user_feed_page(client_conn, database)
			elif (response == "3"):
				user_followers_page(client_conn, database)
			elif (response == "4"):
				user_followings_page(client_conn, database)
			elif (response == "5"):
				user_tweets_page(client_conn, database)
			elif (response == "6"):
				exit_page(client_conn)
		elif (auth == 0):
			client_conn.send(
				bytes(
					"""Login Unsuccessful! Please check your username"""
				, 'utf-8')
			)
		else:
			client_conn.send(
				bytes(
					"""Login Unsuccessful! Please check your password"""
				, 'utf-8')
			)


def exit_page(client_conn):
	""" A function to send exit page to client"""

	while True:
		client_conn.send(
			bytes(
				"""Thanks for using Mini Tweet!"""
			, 'utf-8')
		)
		return
		

def create_account_page(client_conn, database):
	"""A function to handle create account messaging with client"""

	while True:
		client_conn.send(
			bytes(
				"""Enter your username and password:"""
			, 'utf-8')
		)

		username = client_conn.recv(1024).decode()
		password = client_conn.recv(1024).decode()

		db_addlogin(database, username, password)

		client_conn.send(
			bytes(
				"""
				Your account was made successfully!
				Reply with:
				1: to login
				2: to exit
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			login_page(client_conn, database)
		else:
			exit_page(client_conn)



def home_page(client_conn , database):
	"""A function to send home page to client"""

	while True: 
		client_conn.send(
			bytes(
				"""
				Reply with:
				1: for login
				2: for creating account
				3: your profile
				4: exit
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if not response:
			continue
		
		print(response)

		if (response == "1"):
			login_page(client_conn, database)
		elif(response == "2"):
			create_account_page(client_conn, database)
		elif (response == "4"):
			exit_page(client_conn)
			return

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
print('Server listening ... ')

while True:
	# got the connection from client
	connection, addr = s.accept()

	# connection.settimeout(10)

	database = db_load("user")

	home_page(connection, database)

	db_save(database, "user")

	connection.close()
	print("connection closed", repr(addr))

# close the socket object
s.close()
