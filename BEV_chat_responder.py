import socket
import json
import time
from datetime import datetime, timedelta
from pyDes import *

HOSTNAME = socket.gethostname()
BROADCAST_IP = socket.gethostbyname(HOSTNAME)
PEER_DATA_FILE = 'peer_data.json'
CHAT_HISTORY_FILE = 'chat_history.log'

# Diffie-Hellman sabitleri
p = 23
g = 5

with open(PEER_DATA_FILE, 'r') as fp:
    discovered_peers = json.load(fp)
username = discovered_peers[BROADCAST_IP]['username']

# Diffie-Hellman key exchange için fonksiyon
def diffie_hellman_key_exchange(their_key):
    your_random_number = 7  # Rastgele seçilen bir sayı
    your_key = (g ** your_random_number) % p
    shared_key = (their_key ** your_random_number) % p
    return shared_key

def respond_to_chat_request():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 6001))
        s.listen()
        print("Chat Responder is listening...")
        while True:
            conn, addr = s.accept()

            with conn:
                print(f"Connected to {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = json.loads(data.decode())

                    if 'key' in message:  # Diffie-Hellman key exchange
                        their_key = message['key']
                        shared_key = diffie_hellman_key_exchange(their_key)
                        conn.sendall(json.dumps({'key': shared_key}).encode())
                        print("Sent shared key.")
                    
                    elif 'encrypted_message' in message:  # Secure message reception
                        encrypted_message = message['encrypted_message']
                        decrypted_message = decrypt_message(encrypted_message, shared_key)
                        print(f"Received encrypted message: {decrypted_message}")
                        log_message("RECEIVED (Secure)", username, decrypted_message)
                        
                    
                    elif 'unencrypted_message' in message:  # Insecure message reception
                        unencrypted_message = message['unencrypted_message']
                        print(f"Received unencrypted message: {unencrypted_message}")
                        log_message("RECEIVED (Unsecure)", username, unencrypted_message)
                    
                    else:
                        print("Invalid message format.")
            time.sleep(1)


# Mesajı şifrelemek için fonksiyon
def encrypt_message(message, key):
    # Burada mesajı şifrelemek için kullanılan şifreleme algoritmasını seçebilirsiniz.
    # Bu örnekte, pyDes kütüphanesinin kullanımı gösterilmiştir.
    # Ancak, güvenli bir uygulama geliştirmek için daha güçlü bir şifreleme algoritması tercih edilmelidir.
    # Key'iniz güvenli bir şekilde saklanmalı ve kullanılmalıdır.
    des = des(str(key).encode(), ECB, pad=None, padmode=PAD_PKCS5)
    return des.encrypt(message)

# Mesajı çözmek için fonksiyon
def decrypt_message(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():  # Decrypt only alphabetic characters
            shifted = ord(char) - key
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            decrypted_message += chr(shifted)
        else:
            decrypted_message += char
    return decrypted_message

def log_message(action, username, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(CHAT_HISTORY_FILE, 'a') as fp:
        fp.write(f"{timestamp} | {action} | {username} | {message}\n")

if __name__ == "__main__":
    respond_to_chat_request()