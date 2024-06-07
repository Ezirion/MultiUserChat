#!/usr/bin/env python3

import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText



def client_program():

    host = 'localhost'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input(f"\n[+] Introduce tu usuario: ") # Aqui se puede cambiar por algo en tkinter
    print(f"\n Nombre: {username}")
    client_socket.sendall(username.encode())
    create_window(username, client_socket)
    client_socket.close()

def create_window(username, client_socket):

    window = Tk()
    window.title("Chat")

    text_widget = ScrolledText(window, state='disabled')
    text_widget.pack(padx=5, pady=5)

    thread = threading.Thread(target=recv_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    entry_widget = Entry(window)
    entry_widget.pack(pady=5, padx=5, fill=BOTH)
    entry_widget.bind("<Return>", lambda _: send_message(username, client_socket, text_widget, entry_widget))

    window.mainloop()


def send_message(username, client_socket, text_widget, entry_widget): # print("\n[+] Se ha presionado la tecla <Enter>")

    message = entry_widget.get()
    client_socket.sendall(f"{username}: '{message}'\n".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username}: '{message}'\n")
    text_widget.configure(state='disabled')


def recv_message(client_socket, text_widget):

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.configure(state='disabled')
        except:
            break


if __name__ == '__main__':
    client_program()

