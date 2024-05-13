- Networked Peer-to-Peer Chat Application -

Introduction:

This project implements a networked peer-to-peer chat application as part of the course project for CMP 2204 - Introduction to Computer Networks. The application consists of four processes: Peer_Discovery, Service_Announcer, Chat_Responder, and Chat_Initiator. Each responsible for different functionalities of the chat application.

Functionality:

PeerDiscovery: Discovers other users in the local area network by listening to broadcast messages.
ServiceAnnouncer: Announces the availability of the user's chat service to other peers in the network.
ChatResponder: Listens for incoming chat requests, handles key exchange using the Diffie-Hellman algorithm, and decrypts incoming messages.
ChatInitiator: Initiates chats with other users, provides options for secure or insecure chat, and logs chat history.

Usage:

Run service_announcer.py to announce the availability of the chat service.
Run peer_discovery.py to discover other users in the local area network.
Once peers are discovered, run chat_responder.py to listen for incoming chat requests and chat_initiator.py to initiate chats with other users.

Known Limitations:

Single Local Area Network (LAN) Support: The application currently only supports communication within a single local area network. Peers must be connected to the same LAN to discover and communicate with each other.
No User Authentication: The application does not implement user authentication mechanisms. It assumes all peers are trusted and does not verify the identity of users.
Limited Error Handling: Error handling in the application is limited. It may not gracefully handle all possible error scenarios and exceptions.

Dependencies:

Python 3.x
pyDes library for encryption (install via pip install pyDes)

Notes:

Ensure that the dependencies are installed before running the application.
Each process should be run on a separate terminal window or in the background.
Peer data and chat history are stored in peer_data.json and chat_history.log files, respectively.
For secure chat functionality, ensure that both parties agree on the same Diffie-Hellman parameters (p and g) and exchange keys securely.

Contributors:

Volkan Alkan 1903206
Burak Özsoy 2200922
Ekin Sarı 2102671
