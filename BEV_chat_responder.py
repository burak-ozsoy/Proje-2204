# chat_responder.py
import socket
import json
import time

HOSTNAME = socket.gethostname()
BROADCAST_IP = socket.gethostbyname(HOSTNAME)
PEER_DATA_FILE = 'peer_data.json'
CHAT_HISTORY_FILE = 'chat_history.log'

with open(PEER_DATA_FILE, 'r') as fp:
                discovered_peers = json.load(fp)
username = discovered_peers[BROADCAST_IP]['username']

def respond_to_chat_request():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 6001))
        s.listen()
        print("Chat Responder is listening...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected to {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                if 'message' in message:
                    received_message = message['message']
                    print(f"Received message: {received_message}")
                    log_message("RECEIVED", username, received_message)
                else:
                    print("Invalid message format.")
            time.sleep(1)

def log_message(action, username, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(CHAT_HISTORY_FILE, 'a') as fp:
        fp.write(f"{timestamp} | {action} | {username} | {message}\n")

if __name__ == "__main__":
    respond_to_chat_request()
