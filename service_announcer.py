import socket
import json
import time
from threading import Thread

# Constants
BROADCAST_IP = '192.168.1.109'  # Adjust based on your local network configuration
BROADCAST_PORT = 6000

def announce_service(username):
    # Setup UDP socket for broadcasting
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    print("Service Announcement started...")
    
    def send_broadcasts():
        while True:
            try:
                # Construct JSON message
                message = json.dumps({'username': username})
                
                # Broadcast message
                udp_socket.sendto(message.encode(), (BROADCAST_IP, BROADCAST_PORT))
                
                # Sleep for 8 seconds before next broadcast
                time.sleep(8)
                
            except KeyboardInterrupt:
                print("Service Announcement stopped.")
                udp_socket.close()
                break
    
    # Start sending broadcasts in a separate thread
    send_thread = Thread(target=send_broadcasts)
    send_thread.start()

    # Keep the main thread running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    username = input("Enter your username: ")
    announce_service(username)

