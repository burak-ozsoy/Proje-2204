# chat_initiator.py
import json
# Import discovered_peers variable from peer_discovery module
from peer_discovery import *
PEER_DATA_FILE = 'peer_data.json'  # File to store discovered peers

def display_available_users():
    with open(PEER_DATA_FILE, 'r') as fp:
        discovered_peers = json.load(fp)
        print("Discovered peers:", discovered_peers)

# Add this function to the __main__ block for testing purposes
if __name__ == "__main__":
    display_available_users()
