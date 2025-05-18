# Example API Requests

## Send Notifications

### 1. Send Combined (Email + SMS) Notification
```bash
curl -X POST "http://localhost:8000/notifications" \
     -H "Content-Type: application/json" \
     -d '{
         "user_id": "user123",
         "types": ["email", "sms"],
         "title": "Test Combined Notification",
         "message": "This is a test notification via both Email and SMS",
         "recipient_email": "user@example.com",
         "recipient_phone": "+1234567890"
     }'
```

### 2. Send Email Only
```bash
curl -X POST "http://localhost:8000/notifications" \
     -H "Content-Type: application/json" \
     -d '{
         "user_id": "user123",
         "types": ["email"],
         "title": "Test Email Notification",
         "message": "This is a test email notification",
         "recipient_email": "user@example.com"
     }'
```

### 3. Send SMS Only
```bash
curl -X POST "http://localhost:8000/notifications" \
     -H "Content-Type: application/json" \
     -d '{
         "user_id": "user123",
         "types": ["sms"],
         "title": "Test SMS Notification",
         "message": "This is a test SMS notification",
         "recipient_phone": "+1234567890"
     }'
```

### 4. Send In-App Notification
```bash
curl -X POST "http://localhost:8000/notifications" \
     -H "Content-Type: application/json" \
     -d '{
         "user_id": "user123",
         "types": ["in_app"],
         "title": "Test In-App Notification",
         "message": "This is a test in-app notification"
     }'
```

## Get User Notifications

### Get All Notifications for a User
```bash
curl "http://localhost:8000/users/user123/notifications"
```

## Example Response Formats

### Successful Response
```json
{
  "ok": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "user123",
      "type": "email",
      "title": "Test Notification",
      "message": "This is a test message",
      "status": "delivered",
      "created_at": "2024-01-01T12:00:00.000Z",
      "recipient_email": "user@example.com",
      "recipient_phone": null
    }
  ]
}
```

### Error Response
```json
{
  "ok": false,
  "error": "Email address is required for email notifications"
}
```

## PowerShell Examples

### Send Combined Notification
```powershell
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    user_id = "user123"
    types = @("email", "sms")
    title = "Test Combined Notification"
    message = "This is a test notification via both Email and SMS"
    recipient_email = "user@example.com"
    recipient_phone = "+1234567890"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/notifications" -Method Post -Headers $headers -Body $body
```

### Get User Notifications
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/users/user123/notifications" -Method Get
```

## Python Examples

### Send Notification
```python
import requests
import json

url = "http://localhost:8000/notifications"
headers = {
    "Content-Type": "application/json"
}
data = {
    "user_id": "user123",
    "types": ["email", "sms"],
    "title": "Test Notification",
    "message": "This is a test message",
    "recipient_email": "user@example.com",
    "recipient_phone": "+1234567890"
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2))
```

## Notes

1. Replace placeholder values:
   - `user123` with actual user ID
   - `user@example.com` with actual email
   - `+1234567890` with actual phone number (international format)

2. All timestamps are in ISO 8601 format

3. Phone numbers must be in international format with country code 