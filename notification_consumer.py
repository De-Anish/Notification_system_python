import asyncio
import json
from aio_pika import IncomingMessage
from rabbitmq_service import RabbitMQService
from main import send_email, send_sms, notifications_store
import traceback

async def process_email(message: IncomingMessage):
    """Process email notifications from queue"""
    try:
        print("\n==== Processing Email Notification ====")
        print(f"Raw message: {message.body.decode()}")
        async with message.process():
            notification = json.loads(message.body.decode())
            print(f"Parsed notification: {notification}")
            print(f"Attempting to send email to: {notification['recipient_email']}")
            success = send_email(
                to_email=notification['recipient_email'],
                subject=notification['title'],
                message=notification['message']
            )
            if success:
                print(f"✓ Email sent successfully to {notification['recipient_email']}")
            else:
                print(f"✗ Failed to send email to {notification['recipient_email']}")
                await message.reject(requeue=True)
    except Exception as e:
        print(f"✗ Error processing email notification:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        await message.reject(requeue=True)

async def process_sms(message: IncomingMessage):
    """Process SMS notifications from queue"""
    try:
        print("\n==== Processing SMS Notification ====")
        print(f"Raw message: {message.body.decode()}")
        async with message.process():
            notification = json.loads(message.body.decode())
            print(f"Parsed notification: {notification}")
            print(f"Attempting to send SMS to: {notification['recipient_phone']}")
            success = send_sms(
                to_phone=notification['recipient_phone'],
                message=f"{notification['title']}\n{notification['message']}"
            )
            if success:
                print(f"✓ SMS sent successfully to {notification['recipient_phone']}")
            else:
                print(f"✗ Failed to send SMS to {notification['recipient_phone']}")
                await message.reject(requeue=True)
    except Exception as e:
        print(f"✗ Error processing SMS notification:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        await message.reject(requeue=True)

async def process_in_app(message: IncomingMessage):
    """Process in-app notifications from queue"""
    try:
        print("\n==== Processing In-App Notification ====")
        print(f"Raw message: {message.body.decode()}")
        async with message.process():
            notification = json.loads(message.body.decode())
            print(f"Parsed notification: {notification}")
            user_id = notification['user_id']
            if user_id not in notifications_store:
                notifications_store[user_id] = []
            notifications_store[user_id].append(notification)
            print(f"✓ In-app notification stored for user {user_id}")
            notification['status'] = 'delivered'
    except Exception as e:
        print(f"✗ Error processing in-app notification:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        await message.reject(requeue=True)

async def main():
    print("\n=== Starting Notification Consumer ===")
    print("Initializing RabbitMQ service...")
    
    rabbitmq = RabbitMQService()
    
    if not await rabbitmq.connect():
        print("✗ Failed to connect to RabbitMQ")
        return
    print("✓ Successfully connected to RabbitMQ")

    print("\nSetting up notification consumers...")
    await rabbitmq.setup_consumer('email_notifications', process_email)
    await rabbitmq.setup_consumer('sms_notifications', process_sms)
    await rabbitmq.setup_consumer('in_app_notifications', process_in_app)

    print("\n✓ Consumer is now running and waiting for messages...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down consumer...")
    finally:
        await rabbitmq.close()

if __name__ == "__main__":
    asyncio.run(main()) 
