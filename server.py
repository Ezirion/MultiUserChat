#!/usr/bin/env python3

import socket
import threading

def client_thread(client_socket, clients, usernames):

    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    print(f"\n[+] El usuario {username} se ha conectado")

    for client in clients:
        if client != client_socket:
            client.sendall(f"-------| El usuario {username} se ha conectado |-------\n".encode())

    while True:
        try:
            data = client_socket.recv(1024)
            for client in clients:
                if client != client_socket:
                    client.sendall(data)
        except:
            continue

def server_program():

    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # TIME_WAIT
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"\n[+] El servidor está en escucha de conexiones entrantes...")

        clients = [] # Lista de sockets de cliente
        usernames = {} # Este dict relacionará el socket del cliente con su nombre de usuario

        while True:

            client_socket, address = server_socket.accept()
            clients.append(client_socket)

            print(f"\n[+] Se ha conectado un nuevo cliente: {address}")

            thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
            thread.daemon = True
            thread.start()

if __name__ == '__main__':
    server_program()
