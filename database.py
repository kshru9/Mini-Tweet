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

	hashtag_category: {
		user: list({
			tweet: string,
			date: date,
			time: time
		})
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

def db_get_user_details(database, username):
	detials = dict()
	detials["followers"] = database[username]["followers"]
	detials["following"] = database[username]["following"]
	detials["tweets"] = database[username]["tweets"]
	return detials

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