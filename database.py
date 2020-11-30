import pickle
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
			}),
		followers: list(),
		following: list()
	},

	hashtag_category:{ 
		hashtag:{
			list({ username:
				tweet: string,
				date: date,
				time: time
			})
		}
	}
}
"""

def db_addlogin(database, username, password):
	database[username] = {
		"password": password,
		"is_logged": False,
		"tweets": list(),
		"followers": list(),
		"following": list()
	}
	print('Added %s to database' %username)
	db_save(database, "user")
	return database
	

def db_load(dbfile):
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

def db_get_user_followers(database, username):
	followers = database[username]["followers"]
	string = ""
	for x in followers:
		string += x
		string += "\n"
	db_save(database, "user")
	return string

def db_get_user_following(database, username):
	followings = database[username]["following"]
	string = ""
	for x in followings:
		string += x
		string += "\n"
	db_save(database, "user")
	return string

def db_get_user_tweets(database, username):
	tweets = database[username]["tweets"]
	string = ""
	for x in tweets:
		string += x["tweet"]
		string += "\n"
	db_save(database, "user")
	return string

def db_get_user(database, username):
	users = list(database.keys())
	if (username in users):
		db_save(database, "user")
		return 1
	db_save(database, "user")
	return 0

def db_follow_user(database, username, parent_user):
	if (username in database[parent_user]["followers"]):
		return 0
	database[parent_user]["followers"].append(username)
	return database

def db_unfollow_user(database, username, parent_user):
	if (username not in database[parent_user]["followers"]):
		return 0
	database[parent_user]["followers"].remove(username)
	return database

def db_delete_tweet(database, username, tweet):
	if (tweet not in database[username]["tweets"]):
		return 0
	database[username]["tweets"].append(tweet)
	return database

def setHash(database,hashtag,username,tweet,date,time):
	if hashtag in database['hashtag_category'].keys() :
		pass
	else:
		database['hashtag_category'][hashtag]=[]
	details={
		'username':username,
		'tweet':tweet,
		'date':date,
		'time':time,
	}
	database['hashtag_category'][hashtag].append(details)
	db_save(database, "user")

def setTweet(database,username,tweet,date,time):
	details={
		'tweet' : tweet,
		'date': date,
		'time': time,
	}
	database[username]['tweets'].append(details)
	db_save(database, "user")
	return database