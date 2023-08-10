import sys
import socket

def send_message(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        print("Connected to the server. Type 'terminate' to exit.")
        
        while True:
            message = input("Enter your message: ")
            client.send(message.encode('utf-8'))
            if message == 'terminate':
                break

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python my_client_app.py <SERVER_IP> <PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    send_message(server_ip, server_port)
