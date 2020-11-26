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

def db_load(dbfile):
	File = open(dbfile, 'rb')
	db = pickle.load(File)
	File.close()
	return db


def db_save(database, filename):
	dbfile = open(filename, 'ab')
	pickle.dump(database, dbfile)
	dbfile.close()

def db_get_user_followers(database, username):
	followers = database[username]["followers"]
	string = ""
	for x in followers:
		string += x
		string += "\n"
	return string

def db_get_user_following(database, username):
	followings = database[username]["following"]
	string = ""
	for x in followings:
		string += x
		string += "\n"
	return string

def db_get_user_tweets(database, username):
	tweets = database[username]["tweets"]
	string = ""
	for x in tweets:
		string += x
		string += "\n"
	return string

def db_get_user(database, username):
	users = list(database.keys())
	if (username in users):
		return 1
	return 0

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

def setTweet(database,username,tweet,date,time):
	if 'tweets' in database[username].keys() :
		pass
	else:
		database[username]['tweets']=[]
	details={
		'tweet' : tweet,
		'date': date,
		'time': time,
	}
	database[username]['tweets'].append(details)