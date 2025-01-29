import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer as Stemmer
import nltk
import socket

nltk.download('stopwords')

# Define the same process function used in the training script
def process(text):
    """Preprocess text by removing punctuation, stopwords, and applying stemming."""
    text = text.lower()  # Lowercase text
    text = ''.join([t for t in text if t not in string.punctuation])  # Remove punctuation
    text = [t for t in text.split() if t not in stopwords.words('english')]  # Remove stopwords
    st = Stemmer()
    text = [st.stem(t) for t in text]  # Apply stemming
    return text

# Path to the saved spam filter model
MODEL_PATH = "model.pkl"

def load_model(path):
    """Load the trained spam filter model."""
    print(f"[DEBUG] Looking for model file at: {os.path.abspath(path)}")
    if not os.path.exists(path):
        print("[ERROR] Model file not found. Please check the file path.")
        exit(1)
    print("[FIREWALL] Loading ML model...")
    model = joblib.load(path)
    print("[FIREWALL] Model loaded successfully.")
    return model

def forward_to_application_server(app_ip, app_port, message):
    """Forward the filtered message to the application server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as app_socket:
        app_socket.connect((app_ip, app_port))
        app_socket.sendall(message.encode())
        print(f"[FIREWALL] Forwarded message to {app_ip}:{app_port}")

def handle_client(client_socket, client_addr, model, app_server_ip, app_server_port):
    """Handle communication with a single client."""
    print(f"[FIREWALL] Handling client {client_addr}...")
    try:
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                print(f"[FIREWALL] Client {client_addr} disconnected.")
                break  # Client disconnected

            print(f"[FIREWALL] Received message from {client_addr}: {data}")
            
            # Process the message immediately
            prediction = model.predict([data])[0]
            if prediction == "ham":
                print("[FIREWALL] Message classified as HAM. Forwarding to application server...")
                forward_to_application_server(app_server_ip, app_server_port, data)
            else:
                print("[FIREWALL] Message classified as SPAM. Dropped.")
    except Exception as e:
        print(f"[ERROR] Error with client {client_addr}: {e}")
    finally:
        print(f"[FIREWALL] Connection with {client_addr} closed.")
        client_socket.close()

def start_firewall(firewall_ip, firewall_port, app_server_ip, app_server_port):
    """Start the firewall to filter SMTP traffic."""
    # Load the machine learning model
    model = load_model(MODEL_PATH)

    print("[FIREWALL] Firewall node is running...")

    # Set up the firewall server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as firewall_socket:
        firewall_socket.bind((firewall_ip, firewall_port))
        firewall_socket.listen(5)
        print(f"[FIREWALL] Listening on {firewall_ip}:{firewall_port}...")

        while True:
            client_socket, client_addr = firewall_socket.accept()
            handle_client(client_socket, client_addr, model, app_server_ip, app_server_port)

# Main execution
if __name__ == "__main__":
    FIREWALL_IP = "firewall"
    FIREWALL_PORT = 8888    
    APP_SERVER_IP = "application"
    APP_SERVER_PORT = 9090

    start_firewall(FIREWALL_IP, FIREWALL_PORT, APP_SERVER_IP, APP_SERVER_PORT)
