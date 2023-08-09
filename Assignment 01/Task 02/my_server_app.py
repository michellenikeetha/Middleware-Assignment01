import sys
import socket
import threading

def handle_client(client_socket, client_address, clients):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Received from {client_address[0]}:{client_address[1]}: {message}")
        
        for c in clients:
            if c['mode'] == 'SUBSCRIBER':
                c['socket'].send(message.encode('utf-8'))

    client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server listening on port {port}...")

    clients = []

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        mode = client_socket.recv(1024).decode('utf-8')
        print(f"Client mode is {mode}")
        clients.append({'socket': client_socket, 'address': client_address, 'mode': mode})
        
        if mode == 'PUBLISHER':
            publisher_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, clients,))
            publisher_handler.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
