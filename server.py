import socket
import threading
# from _thread import *
import pickle
from utils import *
from database import *
import datetime
import re

def post_receive(client_conn,database,username):

	tweet=''
	tweet_part=str((client_conn.recv(1024)).decode('utf-8'))
	while tweet_part :
		tweet+=tweet_part
		tweet_part=str((client_conn.recv(1024)).decode('utf-8'))

	dt_object=datetime.now()
	date=dt_object.date
	time=dt_object.time

	hashtags=re.findall(r'#\w+') #creates a list of hashtags in the tweet
	for hash in hashtags:
		setHash(database,hash,username,tweet,date,time)
	followers = db_get_user_following(database, username)
	
	setTweet(database,username,tweet,date,time)

def search_user_page(client_conn , database, username):
	"""A Function to send search user page to client"""

	while True:
		client_conn.send(
			bytes(
				"""Enter the username you want to search for:"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (db_get_user(database, response)):
			client_conn.send(
				bytes(
					"""User Found !
						Reply with:
						1: To get profile page of searched user
						2: To get all tweets of searched user
						3: To get all followers of searched user
						4: To get all followings of searched user
						5: Your feed
					"""
				, 'utf-8')
			)

			response = client_conn.recv(1024).decode()

			if (response == "1"):
				user_profile_page(client_conn, database, response)
			elif (response == "2"):
				user_tweets_page(client_conn, database, response)
			elif (response == "3"):
				user_followers_page(client_conn, database, response)
			elif (response == "4"):
				user_followings_page(client_conn, database, response)
			elif (response == "5"):
				user_feed_page(client_conn, database, username)
		else:
			client_conn.send(
				bytes(
					"""User Not Found !
						Reply with:
						1: Your Profile page
						2: Your feed
						3: Your followings
						4: Your tweets
						5: Post Tweet
						6: Search User Again
						7: Your Followers
						8: Log out (Please do not click this!)
					"""
				, 'utf-8')
			)

			response = client_conn.recv(1024).decode()

			if (response == "1"):
				user_profile_page(client_conn, database, response)
			elif (response == "2"):
				user_feed_page(client_conn, database, response)
			elif (response == "3"):
				user_followings_page(client_conn, database, response)
			elif (response == "4"):
				user_tweets_page(client_conn, database, username)
			elif (response == "5"):
				user_post_tweet(client_conn, database, username)
			elif (response == "6"):
				search_user_page(client_conn, database, username)
			elif (response == "7"):
				user_followers_page(client_conn, database, response)
			elif (response == "8"):
				logout_page(client_conn, database, username)

def user_profile_page(client_conn, database, username):
	"""A function to send profile page to the client"""

	while True:
		details = db_get_user_details(database, username)
		
		followers = db_get_user_followers(database, username)
		
		profile_message = """Your Profile details"""
		client_conn.send(
			bytes(
				"""Your Profile details:
					Username: 
				""" + username
				"""Followers: """ + followers +
				"""Followings:""" + followings +
				
			, 'utf-8')
		)
		
def user_feed_page(client_conn, database, username):

def user_follower_detail(client_conn, database, username, parent_user):
	"""A function to send details of requested follower of client to client"""
	while True:
		tweets = db_get_user_tweets(database, username)
		followers = db_get_user_followers(database, username)
		followings = db_get_user_following(database, username)
		
		client_conn.send(
			bytes(
				"Profile page of " + username + 
				"""Followers: """ + followers +
				"""Followings:""" + followings +
				"""Tweets:""" + tweets + 
				"""Reply with:
				1: Follow
				2: Your Feed
				3: Your profile page
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			database[username]["followers"].append(parent_user)
			database[parent_user]["followings"].append(username)
		elif (response == "2"):
			user_feed_page(client_conn, database, parent_user)
		elif (response == "3"):
			user_profile_page(client_conn, database, parent_user)

def user_following_detail(client_conn, database, username, parent_user):
	"""A function to send details of requested follower of client to client"""
	while True:
		tweets = db_get_user_tweets(database, username)
		followers = db_get_user_followers(database, username)
		followings = db_get_user_following(database, username)
		
		client_conn.send(
			bytes(
				"Profile page of " + username + 
				"""Followers: """ + followers +
				"""Followings:""" + followings +
				"""Tweets:""" + tweets + 
				"""Reply with:
				1: Unfollow
				2: Your Feed
				3: Your profile page
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			database[parent_user]["followings"].remove(username)
			database[username]["followers"].remove(parent_user)
		elif (response == "2"):
			user_feed_page(client_conn, database, parent_user)
		elif (response == "3"):
			user_profile_page(client_conn, database, parent_user)

def user_followers_page(client_conn, database, username):
	"""A function to send page containing its followers to client"""
	while True:
		followers = db_get_user_followers(database, username)

		client_conn.send(
			bytes(
				"""Your Followers are:
				""" + followers +
				"""Reply with:
					1: Profile page
					2: Your feed
					3: Your followings
					4: Your tweets
					5: Post Tweet
					6: Search User
					7: Log out (Please do not click this!) 
				""" +
				""" or Enter name of follower to get details"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			user_profile_page(client_conn, database, username)
		elif (response == "2"):
			user_feed_page(client_conn, database, username)
		elif (response == "3"):
			user_followings_page(client_conn, database, username)
		elif (response == "4"):
			user_tweets_page(client_conn, database, username)
		elif (response == "5"):
			user_post_tweet(client_conn, database, username)
		elif (response == "6"):
			search_user(client_conn, database, username)
		elif (response == "7"):
			logout_page(client_conn, database, username)
		else:
			user_follower_detail(client_conn, database, response, username)

def user_followings_page(client_conn, database, username):
	"""A function to send page containing all people it is following to client"""
	while True:
		followers = db_get_user_following(database, username)

		client_conn.send(
			bytes(
				"""People whom you follow are:
				""" + followers +
				"""Reply with:
					1: Profile page
					2: Your feed
					3: Your followings
					4: Your tweets
					5: Post Tweet
					6: Search User
					7: Log out (Please do not click this!) 
				""" +
				""" or Enter username of followings to get details"""
			, 'utf-8')
		)

def user_tweets_page(client_conn, database, username):
	"""A function to send page containing all its tweets to client"""
	
	tweets = db_get_user_tweets(database, username)
	
	while True:	

		client_conn.send(
			bytes(
				"""Your Tweets are:
				""" + tweets +
				""" Reply with:
					1: Profile page
					2: Your feed
					3: Your followings
					4: Delete tweets
					5: Post Tweet
					6: Search User
					7: Log out (Please do not click this!)
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			user_profile_page(database, username, tweet)
		elif (response == "2"):
			user_feed_page(client_conn, database, username)
		elif (response == "3"):
			user_followings_page(client_conn, database, username)
		elif (response == "4"):
			user_delete_tweets(client_conn, database, username)
		elif (response == "5"):
			user_post_tweet(client_conn, database, username)
		elif (response == "6"):
			search_user_page(client_conn, database, username)
		elif (response == "7"):
			logout_page(client_conn, database, username)

def logout_page(client_conn, database, username):
	"""A function to logout client"""
	
	while True:
		database[username]["is_logged"] = False

		client_conn.send(
			bytes(
				"""You have been successfully logged out!
					See you soon!
				"""
			, 'utf-8')
		)
		return

def exit_page(client_conn):
	""" A function to send exit page to client"""

	while True:
		client_conn.send(
			bytes(
				"""Thanks for using Mini Tweet!"""
			, 'utf-8')
		)
		return

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
			
			database[username]["is_logged"] = True
			
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
						6: Post Tweet
						7: Search User
						6: Log out (Please do not click this!)
					"""
				, 'utf-8')
			)
			
			response = client_conn.recv(1024).decode()

			if (response == "1"):
				user_profile_page(client_conn, database, username)
			elif (response == "2"):
				user_feed_page(client_conn, database, username)
			elif (response == "3"):
				user_followers_page(client_conn, database, username)
			elif (response == "4"):
				user_followings_page(client_conn, database, username)
			elif (response == "5"):
				user_tweets_page(client_conn, database, username)
			elif (response == "6"):
				user_post_tweet(client_conn, database, username)
			elif (response == "7"):
				search_user_page(client_conn, database, username)
			elif (response == "8"):
				logout_page(client_conn, database, username)
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