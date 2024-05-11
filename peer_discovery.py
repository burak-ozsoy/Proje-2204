import socket
import json
import time
from threading import Thread

# Sabitler
HOSTNAME = socket.gethostname()
BROADCAST_IP = socket.gethostbyname(HOSTNAME)
BROADCAST_PORT = 6000
PEER_DATA_FILE = 'peer_data.json'

def discover_peers():
    discovered_peers = {}
    
    # Yayınları dinlemek için UDP soketi oluştur
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', BROADCAST_PORT))
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    print("Peer Discovery started...")
    
    def receive_broadcasts():
        while True:
            try:
                # Yayın mesajını al
                data, addr = udp_socket.recvfrom(1024)
                
                # JSON verisini ayrıştır
                try:
                    message = json.loads(data)
                    username = message.get('username')
                    ip_address = addr[0]
                    
                    # Zaman damgasını güncelle
                    discovered_peers[ip_address] = {
                        'ip':ip_address,
                        'username': username,
                        'timestamp': time.time()
                    }
                    
                    # Dosyaya kaydet
                    with open(PEER_DATA_FILE, 'w') as fp:
                        json.dump(discovered_peers, fp)
                    
                    # Alınan kullanıcıyı ekrana yazdır
                    print(f"Detected user: {username} is online")
                    print("Discovered peers:", discovered_peers)
                except json.JSONDecodeError:
                    print("Error parsing JSON data")
                    
            except KeyboardInterrupt:
                print("Peer Discovery stopped.")
                udp_socket.close()
                break
    
    # Yayınları almak için ayrı bir iş parçacığında çalıştır
    receive_thread = Thread(target=receive_broadcasts)
    receive_thread.start()
    
    # Ana iş parçacığını çalışır durumda tut
    while True:
        time.sleep(1)

if __name__ == "__main__":
    discover_peers()
