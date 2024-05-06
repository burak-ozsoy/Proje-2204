import socket
import json
import time
from threading import Thread

# Constants
BROADCAST_IP = '192.168.1.255'  # Adjust based on your local network configuration
BROADCAST_PORT = 6000
PEER_DATA_FILE = 'peer_data.json'  # File to store discovered peers

def discover_peers():
    discovered_peers = {}
    
    # Setup UDP socket for receiving broadcasts
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', BROADCAST_PORT))
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    print("Peer Discovery started...")
    
    def receive_broadcasts():
        while True:
            try:
                # Receive broadcast message
                data, addr = udp_socket.recvfrom(1024)
                
                # Parse JSON data
                try:
                    message = json.loads(data)
                    username = message.get('username')
                    ip_address = addr[0]
                    
                    # Update timestamp
                    discovered_peers[ip_address] = {
                        'username': username,
                        'timestamp': time.time()
                    }
                    
                    # Save to file
                    with open(PEER_DATA_FILE, 'w') as fp:
                        json.dump(discovered_peers, fp)
                    
                    # Display detected user
                    print(f"Detected user: {username} is online")
                    print("Discovered peers:", discovered_peers)
                except json.JSONDecodeError:
                    print("Error parsing JSON data")
                    
            except KeyboardInterrupt:
                print("Peer Discovery stopped.")
                udp_socket.close()
                break
    
    # Start receiving broadcasts in a separate thread
    receive_thread = Thread(target=receive_broadcasts)
    receive_thread.start()
    
    # Keep the main thread running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    discover_peers()
