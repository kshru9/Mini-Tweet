def login_auth(database, username, password):
    print(list(database.keys()), "list")
    if (username in list(database.keys())):
        if (database[username]["password"] == password):
            return 1
        else:
            return -1
    return 0