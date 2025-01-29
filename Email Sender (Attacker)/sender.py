import socket
import random
import time  # Import time module for adding delay

# List of sample ham and spam emails
HAM_EMAILS = [
    "Hello John, let's meet tomorrow at 3 PM.",
    "Dear Client, your order has been shipped. Tracking ID: 123456.",
    "Hi! Can you review the attached document and let me know your feedback?",
]

SPAM_EMAILS = [
    "Congratulations! You've won a $1000 gift card. Click here to claim it.",
    "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's",
    "SIX chances to win CASH! From 100 to 20,000 pounds txt> CSH11 and send to 87575. Cost 150p/day, 6days, 16+ TsandCs apply Reply HL 4 info",
]

def generate_email():
    """Generate a random email tagged as spam or ham."""
    is_spam = random.choice([True, False])
    email = random.choice(SPAM_EMAILS if is_spam else HAM_EMAILS)
    return email, is_spam

def send_emails_to_firewall(server_ip, server_port, num_emails=10, delay=2):
    """
    Send generated emails to the Firewall Node with a delay between each email.
    
    :param server_ip: IP address of the Firewall Node
    :param server_port: Port of the Firewall Node
    :param num_emails: Number of emails to send
    :param delay: Delay in seconds between sending emails
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        print("[CLIENT] Connected to Firewall Node.")
        for i in range(num_emails):
            email, is_spam = generate_email()
            message = f"Subject: Simulated Email\n\n{email}"
            print(f"[CLIENT] Sending email {i + 1}/{num_emails}: {message} (Spam: {is_spam})")
            client_socket.sendall(message.encode())
            time.sleep(delay)  # Pause before sending the next email
        print("[CLIENT] All emails sent.")

if __name__ == "__main__":
    FIREWALL_IP = "firewall"
    FIREWALL_PORT = 8888
    NUM_EMAILS = 10  # Number of emails to send
    DELAY_BETWEEN_EMAILS = 5  # Delay in seconds (e.g., 3 seconds)

    send_emails_to_firewall(FIREWALL_IP, FIREWALL_PORT, NUM_EMAILS, DELAY_BETWEEN_EMAILS)
