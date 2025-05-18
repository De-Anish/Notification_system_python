import json
import aio_pika
from typing import Dict, Any, Union
import os
from dotenv import load_dotenv
import traceback
from notification_types import NotificationType  

load_dotenv('example.env')

RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queues = {
            NotificationType.EMAIL: 'email_notifications',
            NotificationType.SMS: 'sms_notifications',
            NotificationType.IN_APP: 'in_app_notifications',
            'email': 'email_notifications',
            'sms': 'sms_notifications',
            'in_app': 'in_app_notifications'
        }

    async def connect(self):
        """Establish connection to RabbitMQ server"""
        try:
            print("\nConnecting to RabbitMQ...")
            self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
            self.channel = await self.connection.channel()
            
            try:
                print("Attempting to delete existing exchange...")
                await self.channel.exchange_delete("notifications")
                print("Successfully deleted existing exchange")
            except Exception as e:
                print(f"Note: Could not delete exchange (this is normal if it doesn't exist): {e}")

            print("Declaring new exchange...")
            self.exchange = await self.channel.declare_exchange(
                "notifications",
                aio_pika.ExchangeType.DIRECT,
                durable=True,
                auto_delete=False
            )
            print("✓ Exchange declared successfully")

            unique_queues = set(self.queues.values())
            
            print("Setting up queues and bindings...")
            for queue_name in unique_queues:
                queue = await self.channel.declare_queue(queue_name, durable=True)
                await queue.bind(
                    exchange=self.exchange,
                    routing_key=queue_name
                )
                print(f"✓ Queue '{queue_name}' declared and bound to exchange")

            print("✓ Successfully connected to RabbitMQ")
            return True
        except Exception as e:
            print(f"✗ Error connecting to RabbitMQ:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            return False

    async def close(self):
        """Close the RabbitMQ connection"""
        if self.connection:
            await self.connection.close()
            print("RabbitMQ connection closed")

    async def publish_notification(self, notification_type: Union[str, NotificationType], notification_data: Dict[str, Any]):
        """Publish notification to appropriate queue"""
        try:
            queue_name = self.queues.get(notification_type)
            if not queue_name:
                raise ValueError(f"Invalid notification type: {notification_type}")

            print(f"\nPublishing {notification_type} notification...")
            print(f"Notification data: {notification_data}")
            
            message = aio_pika.Message(
                body=json.dumps(notification_data).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )

            await self.exchange.publish(
                message,
                routing_key=queue_name
            )

            print(f"✓ Published {notification_type} notification to queue: {queue_name}")
            return True
        except Exception as e:
            print(f"✗ Error publishing notification:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            return False

    async def setup_consumer(self, queue_name: str, callback):
        """Setup a consumer for processing notifications"""
        try:
            print(f"\nSetting up consumer for queue: {queue_name}")
            queue = await self.channel.declare_queue(queue_name, durable=True)
            await queue.bind(
                exchange=self.exchange,
                routing_key=queue_name
            )
            await queue.consume(callback)
            print(f"✓ Consumer setup complete for queue: {queue_name}")
            return True
        except Exception as e:
            print(f"✗ Error setting up consumer for queue {queue_name}:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            return False 
