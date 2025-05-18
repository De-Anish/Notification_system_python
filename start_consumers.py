import subprocess
import sys
import os
from threading import Thread
import time

def run_consumer(consumer_type):
    try:
        print(f"Starting {consumer_type} consumer...")
        subprocess.run([sys.executable, "notification_consumer.py", "--type", consumer_type], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting {consumer_type} consumer: {e}")
    except KeyboardInterrupt:
        print(f"\n{consumer_type} consumer stopped.")

def main():
    print("=== Starting Notification Consumers ===\n")
    
    # Create threads for each consumer
    email_thread = Thread(target=run_consumer, args=("email",))
    sms_thread = Thread(target=run_consumer, args=("sms",))
    
    try:
        # Start both consumers
        email_thread.start()
        print("Email consumer started successfully!")
        
        time.sleep(2)  # Small delay between starts
        
        sms_thread.start()
        print("SMS consumer started successfully!")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping consumers...")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down all consumers...")
        sys.exit(0) 