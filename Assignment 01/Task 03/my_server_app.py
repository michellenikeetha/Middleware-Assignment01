import sys
import socket
import threading

def handle_client(client_socket, client_address, clients):
    client_data = client_socket.recv(1024).decode('utf-8')
    mode, topic = client_data.split()

    print(f"Accepted connection from {client_address[0]}:{client_address[1]} as {mode} with topic '{topic}'")
    clients.append({'socket': client_socket, 'address': client_address, 'mode': mode, 'topic': topic})

    try:
        if mode == 'PUBLISHER':
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from {mode} {client_address[0]}:{client_address[1]} (Topic: {topic}): {message}")

                for c in clients:
                    if c['mode'] == 'SUBSCRIBER' and c['topic'] == topic: 
                        try:
                            c['socket'].send(message.encode('utf-8'))
                        except OSError as e:
                            print(f"Error sending message to subscriber: {e}")
                            continue
        elif mode == 'SUBSCRIBER':
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received from {mode} {client_address[0]}:{client_address[1]} (Topic: {topic}): {message}")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        clients.remove({'socket': client_socket, 'address': client_address, 'mode': mode, 'topic': topic})
        print(f"Connection closed for {mode} {client_address[0]}:{client_address[1]}")

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server listening on port {port}...")

    clients = []

    while True:
        client_socket, client_address = server.accept()
        handler = threading.Thread(target=handle_client, args=(client_socket, client_address, clients,))
        handler.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
