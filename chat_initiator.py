# chat_initiator.py
import socket
import json
import time
import sys

HOSTNAME = socket.gethostname()
BROADCAST_IP = socket.gethostbyname(HOSTNAME) 
PEER_DATA_FILE = 'peer_data.json'
CHAT_HISTORY_FILE = 'chat_history.log'

def display_available_users():
    with open(PEER_DATA_FILE, 'r') as fp:
        discovered_peers = json.load(fp)
        print("Discovered peers:", discovered_peers)

def chat_with_user(username):
    print(f"Initiating chat with {username}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with open(PEER_DATA_FILE, 'r') as fp:
                discovered_peers = json.load(fp)
                if username not in discovered_peers[BROADCAST_IP]['username']:
                    print(f"{username} is not available.")
                    return
            s.connect((BROADCAST_IP, 6001))
            message = input("Enter your message: ")
            s.sendall(json.dumps({'message': message}).encode())
            print("Message sent successfully.")
            log_message("SENT", username, message)
    except ConnectionRefusedError:
        print(f"Failed to connect to {username}.")
        log_message("ERROR", username, "Connection refused")
    except Exception as e:
        print(f"An error occurred: {e}")

def log_message(action, username, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(CHAT_HISTORY_FILE, 'a') as fp:
        fp.write(f"{timestamp} | {action} | {username} | {message}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chat_initiator.py <username>")
    display_available_users()
    target_username = input("Enter the username you want to chat with: ")
    chat_with_user(target_username)
