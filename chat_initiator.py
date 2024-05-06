# chat_initiator.py

# Import discovered_peers variable from peer_discovery module
from peer_discovery import discovered_peers

def display_available_users():
    print("Available users:")
    for ip_address, username in discovered_peers.items():
        print(f"IP Address: {ip_address}, Username: {username}")

# Add this function to the __main__ block for testing purposes
if __name__ == "__main__":
    display_available_users()
