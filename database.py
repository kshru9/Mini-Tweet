import pickle
import os
"""
structure of database
{
	username: {
		password: password,
		is_logged: true,
		tweets: list({
				tweet: string,
				date: date,
				time: time,
				retweet: NA / from username
			}),
		followers: list(),
		following: list()
	},

	hashtag_category:{ 
		hashtag:{
			list({ username:
				tweet: string,
				date: date,
				time: time,
				retweet: NA / from username
			})
		}
	}
}
"""
def db_load(dbfile):
	if (not os.path.isfile("user.pickle")):
		File = open("user.pickle", "wb")
		pickle.dump(dict(), File)
		File.close()
	File = open("user.pickle", 'rb')
	db = pickle.load(File)
	print(db)
	File.close()
	return db

def db_save(database, filename):
	dbfile = open("user.pickle", 'wb')
	pickle.dump(database, dbfile)
	dbfile.close()
	print("saved")

def db_addlogin(database, username, password):
	database[username] = {
		"password": password,
		"is_logged": False,
		"tweets": list(),
		"followers": list(),
		"following": list()
	}
	print('Added %s to database' %username)
	db_save(database, "user.pickle")
	return database

def db_get_user_followers(database, username):
	if (username not in database.keys()):
		return "USERNAME DONOT EXIST"
	followers = database[username]["followers"]
	string = ""
	for x in followers:
		string += x
		string += "\n"
	db_save(database, "user.pickle")
	return string

def db_get_user_following(database, username):
	if (username not in database.keys()):
		return "USERNAME DONOT EXIST"
	followings = database[username]["following"]
	string = ""
	for x in followings:
		string += x
		string += "\n"
	db_save(database, "user.pickle")
	return string

def db_get_user_tweets(database, username):
	if (username not in database.keys()):
		return "USERNAME DONOT EXIST"
	tweets = database[username]["tweets"]
	string = ""
	for x in tweets:
		string += x["tweet"]
		string += "\n"
	db_save(database, "user.pickle")
	return string

def db_get_all_users(database):
	"""returns string of all users registered on mini tweet"""
	users = list(database.keys())
	string = ""
	for x in users:
		string += x
		string += "\n"
	db_save(database, "user.pickle")
	return string

def db_get_user(database, username):
	"""returns 1 if username exist in db"""
	users = list(database.keys())
	users.remove('hashtag_category')
	if (username in users):
		db_save(database, "user.pickle")
		return 1
	db_save(database, "user.pickle")
	return 0

def db_follow_user(database, username, parent_user):
	if (username in database[parent_user]["followers"]):
		return 0
	database[parent_user]["following"].append(username)
	database[username]["followers"].append(parent_user)
	return database

def db_unfollow_user(database, username, parent_user):
	if (username not in database[parent_user]["followers"]):
		return 0
	database[parent_user]["following"].remove(username)
	database[username]["followers"].remove(parent_user)
	return database

def db_delete_tweet(database, username, tweet):
	alltweets = database[username]["tweets"]
	count = 0
	for x in alltweets:
		if (tweet == x["tweet"]):
			del database[username]["tweets"][count]
			print(database)
			return database
		count+=1
	return 0

def db_get_online_users(database):
	allusers = database.keys()
	allusers.remove('hashtag_category')
	string = ""
	for x in allusers:
		if (database[x]["is_logged"] == True):
			string += x
			string += "\n"
	return string

def setHash(database,hashtag,username,tweet,date,time, retweet):
	try:
		if hashtag in database['hashtag_category'].keys():
			pass
		else:
			database['hashtag_category'][hashtag] = list()
	except KeyError:
		database["hashtag_category"] = dict()
	
	details={
		'username':username,
		'tweet':tweet,
		'date':date,
		'time':time,
		'retweet': retweet
	}
	try:
		database['hashtag_category'][hashtag].append(details)
	except KeyError:
		database['hashtag_category'][hashtag] = list()
		database['hashtag_category'][hashtag].append(details)
	
	db_save(database, "user")
	return database

def setTweet(database,username,tweet,date,time, retweet):
	details={
		'tweet' : tweet,
		'date': date,
		'time': time,
		'retweet': retweet
	}
	database[username]['tweets'].append(details)
	db_save(database, "user")
	return database