import socket
import threading
# from _thread import *
import pickle
from utils import *
from database import *
from datetime import datetime
import re

#Searching for particular hashtag
def search_hashtag(client_conn,database,username):
	"""A function to send search hashtag page to client"""
	while True:
		client_conn.send(
				bytes(
					"""Enter hashtag to Search tweets for it""" 
				, 'utf-8')
			)
		hash='#'+client_conn.recv(1024).decode()
		message='Search results for '+hash+'\n'
		if hash in database["hashtag_category"].keys():
			for h in database["hashtag_category"][hash]:
				message+="By "+h[username]+" :-> "+h['tweet'] + '\t'+h['date']+"  "+h['time']+'\n'

		else:
			message=hash+" Not Found"

		client_conn.send(
			bytes(
				message + 
				"""Reply with:
				1: Your profile page
				2: Search hashtag
				"""
				,'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response=="1"):
			user_profile_page(client_conn, database, username)
		elif (response=="2"):
			search_hashtag(client_conn, database, username)

def trending_hashtag(client_conn,database,username):
	"""A function to send trending hashtag page to client"""

	hashStack=[]
	curr_hash_count=0
	top_5=5
	for hash in database['hashtag_category'].keys():
		curr_hash_count+=1
		curr_len=len(hash)
		if(curr_hash_count <=top_5):
			j=curr_hash_count
			while j>0 and curr_len>len(database['hashtag_category'][hashStack[j]]):
				hashStack[j]=hashStack[j-1]
				j-=1
			hashStack[j]=hash
		else:
			j=5
			while j>0 and curr_len>len(database['hashtag_category'][hashStack[j]]):
				hashStack[j]=hashStack[j-1]
				j-=1
			hashStack[j]=hash

	message='\n'
	for hash in hashStack:
		for h in database["hashtag_category"][hash]:
			message+="By "+h[username]+" :-> "+h['tweet'] + '\t'+h['date']+"  "+h['time']+'\n'
	message+="\n"

	while True:
		client_conn.send(
			bytes(
				"""Top 5 trending hashtags are: """ + "\n" + message +
				"""Reply with:
				1: Your profile page
				"""
			, 'utf-8')
		)
		
		response = client_conn.recv(64*1024)
		
		if (response=="1"):
			user_profile_page(client_conn, database, username) 

def user_feed_page(client_conn, database, username):
	"""To display client's tweets and tweets of people client follow (recent 5)"""

	print('feed')
	Tweets=sorted(database[username]['tweets'],key =lambda i: (i['date'],i['time']),reverse=True)
	Tweets=Tweets[0:5]
	followTweets=[]
	for follow in database[username]['following']:
		followTweets=sorted(database[follow]['tweets'],key =lambda i: (i['date'],i['time']),reverse=True)
		Tweets.extend(followTweets[0:5])
	Tweets=sorted(Tweets,key =lambda i: (i['date'],i['time']))
	
	message=''
	#Send Tweets
	for tweet in Tweets:
		message+="By "+username+" :-> "+tweet['tweet'] + '\t'+tweet['date']+"  "+tweet['time']+'\n'
	#print(message)


	while True:
		client_conn.send(
			bytes(
				"""Your Feed is:
				""" + """\n""" + message +
				"""Reply with:
				1: Your profile page
				"""
				,'utf-8')
				)
		response = client_conn.recv(1024).decode()

		if (response=="1"):
			user_profile_page(client_conn, database, username)
	

def post_receive(client_conn,database,username):
	"""A function to send post tweet page to client"""
	while True:
		client_conn.send(
			bytes(
				"""Enter tweet to post"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

	# tweet=''
	# tweet_part=str((client_conn.recv(1024)).decode('utf-8'))
	# while tweet_part :
	# 	tweet+=tweet_part
	# 	tweet_part=str((client_conn.recv(1024)).decode('utf-8'))

		dt_object=datetime.now()
		date=dt_object.strftime("%d/%m/%Y")
		time=dt_object.strftime("%H:%M:%S")

		hashtags=re.findall(r'#\w+', response) # creates a list of hashtags in the tweet
		for hash in hashtags:
			database = setHash(database,hash,username,response,date,time)
		
		database = setTweet(database,username,response,date,time)
		client_conn.send(
			bytes(
				"""Tweet posted!
				Reply with:
				1: post another tweet
				2: Your profile page
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response=="1"):
			post_receive(client_conn, database, username)
		elif (response=="2"):
			user_profile_page(client_conn, database, username)


def search_user_profile(client_conn, database, username, parent_user):
	"""A Function to send search user profile page to client"""

	while True:
		followers = db_get_user_followers(database, username)
		followings = db_get_user_following(database, username)
		
		client_conn.send(
			bytes(
				"""Profile details:
					Username: 
				""" + username +
				"""Followers: """ + followers +
				"""Followings:""" + followings +
				"""Reply with:
				1: Search User
				2: Follow this user
				3: Unfollow this user
				4: chat with the user
				5: Your profile page
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			search_user_page(client_conn, database, parent_user)
		elif (response == "2"):
			temp = db_follow_user(database, username, parent_user)
			if (temp == 0):
				client_conn.send(bytes("You already follow this user Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn, database, parent_user)
			else:
				database = temp
				client_conn.send(bytes("User followed! Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn, database, parent_user)
		elif (response == "3"):
			temp = db_unfollow_user(database, username, parent_user)
			if (temp == 0):
				client_conn.send(bytes("You do not follow this user. Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn, database, parent_user)
			else:
				database = temp
				client_conn.send(bytes("User unfollowed! Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn, database, parent_user)
		elif (response == "4"):
			user_tweets_page(client_conn, database, username)
		elif (response == "5"):
			user_profile_page(client_conn, database, parent_user)

def search_user_page(client_conn , database, username):
	"""A Function to send search user page to client"""

	while True:
		allusers = db_get_all_users(database)
		
		client_conn.send(
			bytes(
				allusers + " " + 
				"""Enter the username you want to search for:"""
			, 'utf-8')
		)

		search_user = client_conn.recv(1024).decode()

		if (db_get_user(database, search_user)):
			client_conn.send(
				bytes(
					"""User Found !
						Reply with:
						1: To get profile page of searched user
						2: To get all tweets of searched user
						3: To get all followers of searched user
						4: To get all followings of searched user
						5: Your profile page
					"""
				, 'utf-8')
			)

			response = client_conn.recv(1024).decode()

			if (response == "1"):
				search_user_profile(client_conn, database, search_user, username)
			elif (response == "2"):
				user_tweets_page(client_conn, database, search_user)
			elif (response == "3"):
				user_followers_page(client_conn, database, search_user)
			elif (response == "4"):
				user_followings_page(client_conn, database, search_user)
			elif (response == "5"):
				user_profile_page(client_conn, database, username)
		else:
			client_conn.send(
				bytes(
					"""User Not Found !
						Reply with:
						1: Your Profile page
					"""
				, 'utf-8')
			)

			response = client_conn.recv(1024).decode()

			if (response == "1"):
				user_profile_page(client_conn, database, username)
		
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
				2: Your profile page
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			temp = db_follow_user(database, username, parent_user)
			if (temp==0):
				client_conn.send(bytes("You already follow this user. Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn,database,parent_user)
			else:
				database = temp
				client_conn.send(bytes("User Followed. Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn,database,parent_user)
		elif (response == "2"):
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
				2: Your profile page
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			temp = db_unfollow_user(database, username, parent_user)
			if (temp == 0):
				client_conn.send(bytes("You do not follow this user. Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn,database,parent_user)
			else:
				database = temp
				client_conn.send(bytes("Unfollowed user. Reply with: 1: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response=="1"):
					user_profile_page(client_conn,database,parent_user)
		elif (response == "2"):
			user_profile_page(client_conn, database, parent_user)

def user_followers_page(client_conn, database, username):
	"""A function to send page containing its followers to client"""
	while True:
		followers = db_get_user_followers(database, username)

		client_conn.send(
			bytes(
				"""Your Followers are:
				""" + followers +
				""" Enter name of follower to get details"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		user_follower_detail(client_conn, database, response, username)

def user_followings_page(client_conn, database, username):
	"""A function to send page containing all people it is following to client"""
	while True:
		followers = db_get_user_following(database, username)

		client_conn.send(
			bytes(
				"""People whom you follow are:
				""" + followers +
				"""Enter username of any of your followings to get details"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		user_following_detail(client_conn, database, response, username)

def user_tweets_page(client_conn, database, username):
	"""A function to send page containing all its tweets to client"""
	
	tweets = db_get_user_tweets(database, username)
	
	while True:	

		client_conn.send(
			bytes(
				"""Your Tweets are:
				""" + tweets +
				""" Enter tweet to delete it
				""" + 
				"""or Reply with:
				1: Post tweet
				2: Your profile page
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response=="1"):
			post_receive(client_conn, database, username)
		elif (response=="2"):
			user_profile_page(client_conn, database, username)
		else:
			temp = db_delete_tweet(database, username, response)
			if (temp == 0):
				client_conn.send(bytes("The tweet you entered do not exist. Reply with: 1: try again 2: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response == "1"):
					continue
				else:
					user_profile_page(client_conn, database, username)
			else:
				database = temp
				client_conn.send(bytes("Tweet Deleted. Reply with: 1: Delete another 2: Your profile page", 'utf-8'))
				response = client_conn.recv(1024).decode()
				if (response == "1"):
					continue
				else:
					user_profile_page(client_conn, database, username)

def logout_page(client_conn, database, username):
	"""A function to logout client"""
	
	# while True:
	database[username]["is_logged"] = False

	# client_conn.send(
	# 	bytes(
	# 		"""You have been successfully logged out!
	# 			See you soon!
	# 		"""
	# 	, 'utf-8')
	# )

	client_conn.send(
		bytes(
			"""You have been successfully logged out!
				See you soon!
				Where you want to see next?
				Reply with:
				1: Home Page
				2: Exit Page 
			"""
		, 'utf-8')
		)
		
	response = client_conn.recv(1024).decode()

	if (response == "1"):
		home_page(client_conn, database)
		return
	elif(response == "2"):
		exit_page(client_conn, database)
		return
	return

def exit_page(client_conn):
	""" A function to send exit page to client"""
	client_conn.send(
		bytes(
			"""Thanks for using Mini Tweet!"""
		, 'utf-8')
	)
	return


def user_profile_page(client_conn, database, username):
	"""A function to send profile page to the client"""

	while True:
		followers = db_get_user_followers(database, username)
		followings = db_get_user_following(database, username)
		
		profile_message = """Your Profile details"""
		client_conn.send(
			bytes(
				"""Your Profile details:
					Username: 
				""" + username +
				"""Followers: """ + followers +
				"""Followings:""" + followings +
				"""Reply with:
				1: Search User
				2: Your feed
				3: Your tweets
				4: Post Tweet
				5: Log out (We will miss you!)
				6: Search Tweets with hashtag
				7: Get Trending hashtag
				"""
			, 'utf-8')
		)

		response = client_conn.recv(1024).decode()

		if (response == "1"):
			search_user_page(client_conn, database, username)
		elif (response == "2"):
			user_feed_page(client_conn, database, username)
		elif (response == "3"):
			user_tweets_page(client_conn, database, username)
		elif (response == "4"):
			post_receive(client_conn, database, username)
		elif (response == "5"):
			logout_page(client_conn, database, username)
			return
		elif (response=="6"):
			search_hashtag(client_conn, database, username)
		elif(response=="7"):
			trending_hashtag(client_conn, database, username)

def login_page(client_conn, database):
	"""A function to send login page to client"""

	# while True:
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
					2: Log out (We will miss you!)
				"""
			, 'utf-8')
		)
			
		response = client_conn.recv(1024).decode()

		if (response == "1"):
			user_profile_page(client_conn, database, username)
		elif (response == "2"):
			logout_page(client_conn, database, username)
			return
	elif (auth == 0):
		client_conn.send(
			bytes(
				"""Login Unsuccessful! Please check your username
				Reply with:
				1: to create account
				2: to exit
				"""
			, 'utf-8')
		)
		response = client_conn.recv(1024).decode()
		if (response == "1"):
			create_account_page(client_conn, database)
		elif (response == "2"):
			exit_page(client_conn)
			return
	else:
		client_conn.send(
			bytes(
				"""Login Unsuccessful! Please check your password
				Reply with:
				1: to create account
				2: to exit
				"""
			, 'utf-8')
		)
		response = client_conn.recv(1024).decode()
		if (response == "1"):
			create_account_page(client_conn, database)
		elif (response == "2"):
			exit_page(client_conn)
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

		database = db_addlogin(database, username, password)
		print(database, "after login")

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
			return
		else:
			exit_page(client_conn)
			return



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
			return
		elif(response == "2"):
			create_account_page(client_conn, database)
			return
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
	print(" database saved")
	
	connection.close()
	print("connection closed", repr(addr))

# close the socket object
s.close()