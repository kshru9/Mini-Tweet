import time
import socket

HOST = "localhost"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
print("Connected to Server")

while True:
    conn, addr = client_socket.recvfrom(1024)
    
    conn = conn.decode('utf-8')

    if (conn == "Thanks for using Mini Tweet!"):
        print(conn)
        break
    elif(conn == "Enter your username and password:"):
        print('asking password')
        print("Please" + conn)
        username = bytes(str(input()), 'utf-8')
        password = bytes(str(input()), 'utf-8')
        client_socket.send(username)
        client_socket.send(password)
    else:
        print('else')
        print(conn)

        response = bytes(str(input()), 'utf-8')

        client_socket.send(response)

client_socket.close()
print('Connection closed!')

# basic client
