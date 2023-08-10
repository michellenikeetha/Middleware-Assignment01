import sys
import socket
import threading

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Received: {message}")

def send_message(server_ip, server_port, mode, topic):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        client.send(f"{mode} {topic}".encode('utf-8'))  # Send mode and topic to the server
        print(f"Connected to the server in {mode} mode with topic '{topic}'. Type 'terminate' to exit.")

        if mode == 'SUBSCRIBER':
            receiver_thread = threading.Thread(target=receive_messages, args=(client,))
            receiver_thread.start()

        try:
            while True:
                message = input("Enter your message: ")
                client.send(message.encode('utf-8'))
                if message == 'terminate':
                    break
        except KeyboardInterrupt:
            pass  # Catch Ctrl+C and handle it gracefully

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python my_client_app.py <SERVER_IP> <PORT> <MODE> <TOPIC>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    mode = sys.argv[3].upper()
    topic = sys.argv[4]

    send_message(server_ip, server_port, mode, topic)
