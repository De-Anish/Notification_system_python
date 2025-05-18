# Essential Commands for Notification System

## Security Note
⚠️ **IMPORTANT**: Never commit sensitive information to Git:
- API keys
- Passwords
- Access tokens
- Private email addresses
- Phone numbers
- Secret keys

## Initial Setup Commands

### Install Dependencies
```bash
pip install fastapi uvicorn python-multipart aio-pika python-jose[cryptography] passlib[bcrypt] python-dotenv requests twilio
```

### Environment Variables Setup
1. Copy `example.env` to `.env`
```bash
cp example.env .env
```
2. Edit `.env` with your credentials:
```env
# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=<YOUR_EMAIL>
EMAIL_PASSWORD=<YOUR_APP_PASSWORD>

# Twilio Settings
TWILIO_ACCOUNT_SID=<YOUR_ACCOUNT_SID>
TWILIO_AUTH_TOKEN=<YOUR_AUTH_TOKEN>
TWILIO_PHONE_NUMBER=<YOUR_TWILIO_NUMBER>
```

## Git Security Commands

### Check for Sensitive Data
```bash
# Search for potential passwords or tokens
git grep -l "password"
git grep -l "token"
git grep -l "secret"

# Check .env files
git check-ignore .env
```

### If Sensitive Data Was Committed
```bash
# Remove sensitive file from git history
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch path/to/sensitive/file" --prune-empty --tag-name-filter cat -- --all

# Force push changes
git push origin --force --all
```

## RabbitMQ Commands

### Start RabbitMQ Service
```bash
net start RabbitMQ
```

### Stop RabbitMQ Service
```bash
net stop RabbitMQ
```

### Check RabbitMQ Status
```bash
rabbitmqctl status
```

### Enable RabbitMQ Management Plugin
```bash
rabbitmq-plugins enable rabbitmq_management
```

### View RabbitMQ Logs
```bash
rabbitmqctl log_tail
```

## Application Start Commands

### Method 1: Start All Services (Recommended)
```bash
# Run as Administrator
start_all.bat
```

### Method 2: Start Services Individually

1. **Start FastAPI Backend**
```bash
python -m uvicorn main:app --reload --port 8000
```

2. **Start Email Consumer**
```bash
python notification_consumer.py --type email
```

3. **Start SMS Consumer**
```bash
python notification_consumer.py --type sms
```

4. **Start Both Consumers**
```bash
python start_consumers.py
```

## Access Points

1. Frontend UI: Open `index.html` in browser
2. RabbitMQ Dashboard: http://localhost:15672
   - Username: guest
   - Password: guest
3. FastAPI Documentation: http://localhost:8000/docs

## Troubleshooting Commands

### Check RabbitMQ Connection
```bash
# Check if port is in use
netstat -ano | findstr :5672

# Check if service is running
sc query RabbitMQ
```

### Reset RabbitMQ (If Issues Persist)
```bash
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app
```

### Check Erlang Cookie
```bash
# View cookie content
type "%HOMEDRIVE%%HOMEPATH%\.erlang.cookie"
type "C:\Windows\System32\config\systemprofile\.erlang.cookie"
```

## Development Commands

### Create Requirements File
```bash
pip freeze > requirements.txt
```

### Install Requirements
```bash
pip install -r requirements.txt
```

### Run in Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
``` 
