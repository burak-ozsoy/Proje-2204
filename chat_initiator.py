import socket
import json
import time
from datetime import datetime, timedelta
import sys

HOSTNAME = socket.gethostname()
BROADCAST_IP = socket.gethostbyname(HOSTNAME)
PEER_DATA_FILE = 'peer_data.json'
CHAT_HISTORY_FILE = 'chat_history.log'

# def display_available_users():
#     with open(PEER_DATA_FILE, 'r') as fp:
#         discovered_peers = json.load(fp)
#         usernames = [peer_data['username'] for peer_data in discovered_peers.values()]
#         print("Discovered usernames:", usernames)

def display_available_users():
    current_time = datetime.now()
    with open(PEER_DATA_FILE, 'r') as fp:
        discovered_peers = json.load(fp)
        print("Available Users:")
        for ip, peer_data in discovered_peers.items():
            last_broadcast_time = datetime.fromtimestamp(peer_data['timestamp'])
            time_difference = current_time - last_broadcast_time
            if time_difference <= timedelta(minutes=15):
                username = peer_data['username']
                status = "Online" if time_difference <= timedelta(seconds=10) else "Away"
                print(f"{username} ({status})")


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

def menu():
    print("Select an option:")
    print("1. View online users")
    print("2. Initiate chat")
    print("3. View chat history")
    print("4. Exit")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            display_available_users()
        elif choice == '2':
            target_username = input("Enter the username you want to chat with: ")
            chat_with_user(target_username)
        elif choice == '3':
            with open(CHAT_HISTORY_FILE, 'r') as fp:
                print("Chat History:")
                print(fp.read())
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")