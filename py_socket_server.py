# server to receive socket TCP messages and print them to console, and respond

import socket
HOST = '192.168.0.5'  # IP of your computer
PORT = 1701        # Port to listen on 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(data)
            user_input = input("Enter response: ")
            conn.sendall(user_input.encode('utf-8'))



