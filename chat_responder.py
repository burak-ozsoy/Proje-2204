# chat_responder.py
import socket
import json
import time

CHAT_HISTORY_FILE = 'chat_history.log'  # File to store chat history

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
                    log_message("RECEIVED", addr[0], received_message)
                else:
                    print("Invalid message format.")
            time.sleep(1)

def log_message(action, username, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(CHAT_HISTORY_FILE, 'a') as fp:
        fp.write(f"{timestamp} | {action} | {username} | {message}\n")

if __name__ == "__main__":
    respond_to_chat_request()
