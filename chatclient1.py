import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, chat_window):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_window.config(state='normal')
            chat_window.insert('end', message + '\n')
            chat_window.see('end')
            chat_window.config(state='disabled')
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message(client_socket, message_entry, username):
    message = f"{username}: {message_entry.get()}"
    if message:
        try:
            client_socket.send(message.encode('utf-8'))
            message_entry.delete(0, 'end')
        except Exception as e:
            print(f"Error sending message: {e}")

def start_client():
    host = input("Enter the server IP address: ")  
    port = 5555

    # Get username from user input
    username = input("Enter your username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Unable to connect to the server: {e}")
        return

    root = tk.Tk()
    root.title("Chat Application")

    chat_window = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
    chat_window.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.E + tk.S + tk.W)

    message_entry = tk.Entry(root, width=50)
    message_entry.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E + tk.W)

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client_socket, message_entry, username))
    send_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, chat_window))
    receive_thread.start()

    # Display the username in the chat box
    chat_window.config(state='normal')
    chat_window.insert('end', f"Welcome, {username}!\n")
    chat_window.config(state='disabled')

    root.mainloop()

if __name__ == "__main__":
    start_client()
