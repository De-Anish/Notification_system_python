# Notification System

A FastAPI-based notification service that supports Email, SMS, and In-App notifications with message queuing using RabbitMQ.

## Features

- Email notifications using SMTP
- SMS notifications using Twilio
- In-App notifications with message queuing
- RabbitMQ integration for reliable message delivery
- Retry mechanism for failed notifications
- Environment variable configuration
- CORS support
- Modern frontend interface
- Real-time notification status updates

## Prerequisites

- Python 3.8+
- RabbitMQ Server 4.1.0+
- Erlang OTP
- SMTP Server access (for emails)
- Twilio account (for SMS)

## Setup

1. **Clone the repository**
```bash
git clone [repository-url]
cd [repository-name]
```

2. **Install Python dependencies**
```bash
pip install fastapi uvicorn python-multipart aio-pika python-jose[cryptography] passlib[bcrypt] python-dotenv requests twilio
```

3. **Environment Setup**
Create a `.env` file by copying `.env.example`:

```env
# RabbitMQ Configuration
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

## Running the Service

### Method 1: Using Start Script (Recommended)
```bash
start_all.bat  # Run as Administrator
```

### Method 2: Manual Start
1. **Start RabbitMQ Server**
```bash
net start RabbitMQ
```

2. **Start FastAPI Backend**
```bash
python -m uvicorn main:app --reload --port 8000
```

3. **Start Notification Consumers**
```bash
python start_consumers.py
```

## API Endpoints

### Send Notification
`POST /notifications`

Request body:
```json
{
    "user_id": "user123",
    "types": ["email", "sms", "in_app"],
    "title": "Test Notification",
    "message": "This is a test notification",
    "recipient_email": "user@example.com",
    "recipient_phone": "+1234567890"
}
```

### Get User Notifications
`GET /users/{user_id}/notifications`

Returns all notifications for a specific user.

## Example Usage

### Python
```python
import requests

url = "http://localhost:8000/notifications"
payload = {
    "user_id": "user123",
    "types": ["email", "sms", "in_app"],
    "title": "Test Notification",
    "message": "This is a test notification",
    "recipient_email": "user@example.com",
    "recipient_phone": "+1234567890"
}

response = requests.post(url, json=payload)
print(response.json())
```

### cURL
```bash
curl -X POST "http://localhost:8000/notifications" \
     -H "Content-Type: application/json" \
     -d '{
         "user_id": "test_user1",
         "types": ["email", "sms", "in_app"],
         "title": "Test Combined Notification",
         "message": "This is a test notification via Email, SMS and In-App",
         "recipient_email": "user@example.com",
         "recipient_phone": "+1234567890"
     }'
```

## Access Points

- Frontend UI: Open `index.html` in browser
- RabbitMQ Dashboard: http://localhost:15672 (guest/guest)
- FastAPI Docs: http://localhost:8000/docs

## Environment Variables

| Variable | Description |
|----------|-------------|
| RABBITMQ_URL | RabbitMQ connection URL |
| EMAIL_HOST | SMTP server host (e.g., smtp.gmail.com) |
| EMAIL_PORT | SMTP server port (e.g., 587) |
| EMAIL_USERNAME | Email address for sending notifications |
| EMAIL_PASSWORD | Email service app-specific password |
| TWILIO_ACCOUNT_SID | Twilio Account SID |
| TWILIO_AUTH_TOKEN | Twilio Auth Token |
| TWILIO_PHONE_NUMBER | Twilio Phone Number (in international format) |

## Security Notes

- Never commit `.env` file with real credentials
- Use environment variables for sensitive information
- Keep your API keys and tokens secure
- Use app-specific passwords for email services
- Enable 2FA for better security
- Store the `.erlang.cookie` securely for RabbitMQ

## Troubleshooting

### RabbitMQ Connection Issues
1. Verify RabbitMQ is running:
```bash
rabbitmqctl status
```

2. Check RabbitMQ logs:
```bash
rabbitmqctl log_tail
```

3. Ensure Erlang cookie is consistent:
- Check cookie at: `C:\Windows\System32\config\systemprofile\.erlang.cookie`
- Should match: `C:\Users\[YourUsername]\.erlang.cookie`

### Consumer Issues
1. Check consumer logs in terminal
2. Verify RabbitMQ queues in dashboard
3. Check email/SMS credentials in .env file

## Screenshots

### RabbitMQ Dashboard
*Add screenshot showing RabbitMQ dashboard with active queues and message flow*

### Frontend Interface
*Add screenshot of the notification system's frontend interface*

### Email Notification
*Add screenshot of a received email notification*

### SMS Notification
*Add screenshot of a received SMS notification*

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details 