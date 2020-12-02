def login_auth(database, username, password):
    print(list(database.keys()), "list")
    if (username in list(database.keys())):
        if (database[username]["password"] == password):
            return 1
        else:
            return -1
    print("else ps")
    return 0

def encrypt(text,s): 
    result = "" 
  
    # traverse text 
    for i in range(len(text)): 
        char = text[i] 
  
        # Encrypt uppercase characters 
        if (char.isupper()): 
            result += chr((ord(char) + s-65) % 26 + 65) 
  
        # Encrypt lowercase characters 
        else: 
            result += chr((ord(char) + s - 97) % 26 + 97) 
    return result