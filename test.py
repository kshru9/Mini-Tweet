import pickle
def change(x):
    x = 10


d = dict()
dbfile = open("user.pickle", 'ab')
pickle.dump(d, dbfile)
dbfile.close()