import socket
import json
import time
from threading import Thread

# Sabitler
# HOSTNAME = socket.gethostname()
# BROADCAST_IP = socket.gethostbyname(HOSTNAME)  # Yayın yapılacak IP adresi, ağ yapılandırmasına göre ayarlanmalıdır
BROADCAST_IP = "127.0.0.1"
BROADCAST_PORT = 6000


def announce_service(username):
    # Yayın yapmak için UDP soketi oluştur
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    print("Service Announcement started...")
    
    def send_broadcasts():
        while True:
            try:
                # JSON mesajını oluştur
                message = json.dumps({'username': username})
                
                # Yayın mesajını gönder
                udp_socket.sendto(message.encode(), (BROADCAST_IP, BROADCAST_PORT))
                
                # Bir sonraki yayından önce 8 saniye bekleyin
                time.sleep(8)
                
            except KeyboardInterrupt:
                print("Service Announcement stopped.")
                udp_socket.close()
                break
    
    # Yayınları göndermek için ayrı bir iş parçacığında çalıştır
    send_thread = Thread(target=send_broadcasts)
    send_thread.start()

    # Ana iş parçacığını çalışır durumda tut
    while True:
        time.sleep(1)

if __name__ == "__main__":
    username = input("Enter your username: ")
    announce_service(username)
