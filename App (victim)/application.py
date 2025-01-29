import socket

def start_application_server(server_ip, server_port):
    """Start the Application Node server."""
    print("[APPLICATION] Starting Application Node...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen()
        print(f"[APPLICATION] Listening on {server_ip}:{server_port}")
        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                data = client_socket.recv(1024)
                if data:
                    email = data.decode()
                    print(f"[APPLICATION] Received Ham Email:\n{email}\n")

if __name__ == "__main__":
    APP_SERVER_IP = "application"
    APP_SERVER_PORT = 9090
    start_application_server(APP_SERVER_IP, APP_SERVER_PORT)
