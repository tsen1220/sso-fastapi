# SSO FastAPI

A Single Sign-On (SSO) system built with FastAPI, featuring user registration, authentication, and Two-Factor Authentication (2FA/OTP) capabilities.

## 🚀 Features

- **FastAPI** - Modern, fast web framework
- **User Management** - Registration, login, password encryption
- **Two-Factor Authentication** - TOTP/OTP support, compatible with Google Authenticator
- **Redis** - Session management and caching
- **MySQL** - Primary database
- **Docker** - Containerized deployment
- **Alembic** - Database version control

## 🏗 Architecture Overview

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Environment configuration
├── database.py          # Database connection and session management
├── routes/              # API routes
│   ├── user_route.py    # User-related endpoints
│   └── otp_route.py     # OTP-related endpoints
├── services/            # Business logic layer
│   ├── user_service.py  # User service
│   └── otp_key_service.py # OTP service
├── repositories/        # Data access layer
│   ├── user_repository.py
│   └── otp_key_repository.py
├── models/              # SQLAlchemy data models
│   ├── user_model.py    # User model
│   └── otp_key_model.py # OTP key model
├── schemas/             # Pydantic request/response models
│   ├── user_schema.py
│   └── otp_schema.py
└── helpers/             # Utility classes
    └── redis_helper.py  # Redis helper
```

## 📋 System Requirements

- Python 3.9+
- Docker & Docker Compose
- MySQL 8.2+
- Redis 7.4+

## 🛠 Installation & Setup

### Method 1: Docker Compose (Recommended)

1. **Clone the project**
```bash
git clone <repository-url>
cd sso-fastapi
```

2. **Start all services**
```bash
docker-compose up -d
```

This will start:
- Web application (port 8000)
- MySQL database (port 3306)
- Redis cache (port 6379)

3. **Run database migrations**
```bash
# Update alembic configuration in container
docker exec sso-fastapi-web-1 sed -i 's|mysql+pymysql://root:root@localhost/sso-fastapi|mysql+pymysql://root:root@mysql/sso-fastapi|' alembic.ini

# Execute migrations
docker exec sso-fastapi-web-1 alembic upgrade head
```

4. **Verify services are running**
```bash
curl http://localhost:8000/
# Should return: {"Hello":"World"}
```

### Method 2: Local Development

1. **Setup virtual environment**
```bash
python3 -m venv env
source env/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables**
```bash
# Create .env file
cat > app/.env << EOF
DATABASE_URL=mysql+pymysql://root:root@localhost/sso-fastapi
REDIS_HOST=localhost
REDIS_PORT=6379
EOF
```

4. **Start external services**
```bash
# Start only MySQL and Redis
docker-compose up mysql redis -d
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start development server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔄 Database Migrations

### Create New Migration

```bash
# Local development
alembic revision --autogenerate -m "describe your changes"

# Docker environment
docker exec sso-fastapi-web-1 alembic revision --autogenerate -m "describe your changes"
```

### Apply Migrations

```bash
# Local development
alembic upgrade head

# Docker environment  
docker exec sso-fastapi-web-1 alembic upgrade head
```

### Check Migration Status

```bash
# Local development
alembic current
alembic history

# Docker environment
docker exec sso-fastapi-web-1 alembic current
docker exec sso-fastapi-web-1 alembic history
```

## 📚 API Documentation

After starting the application, you can view API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 API Endpoints

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/sign-up` | User registration |
| POST | `/users/login` | User login |

### OTP/2FA Features

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/otp/generate` | Generate OTP key for user |
| POST | `/otp/verify` | Verify OTP code |
| GET | `/otp/{user_id}` | Get user OTP information |
| DELETE | `/otp/{user_id}` | Delete user OTP key |

## 🧪 Testing OTP Functionality

1. **Register a new user**
```bash
curl -X POST "http://localhost:8000/users/sign-up" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

2. **Generate OTP key**
```bash
curl -X POST "http://localhost:8000/otp/generate" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1}'
```

3. **Scan QR code with Google Authenticator**
   - Get `qr_code_uri` from the response
   - Use a QR code generator to create the QR code
   - Scan with Google Authenticator

4. **Verify OTP code**
```bash
curl -X POST "http://localhost:8000/otp/verify" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "otp_code": "123456"}'
```

## 🔧 Development Tools

### Clean Duplicate Dependencies

```bash
pip freeze > requirements_clean.txt
# Manually edit to remove duplicates
mv requirements_clean.txt requirements.txt
```

### Rebuild Docker Containers

```bash
docker-compose down
docker-compose up --build -d
```

### View Logs

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs mysql
docker-compose logs redis
```

## 🐛 Troubleshooting

### Common Issues

1. **Database connection failed**
   - Ensure MySQL container is running
   - Check database URL configuration

2. **Migration failed**
   - Ensure database is accessible
   - Check connection string in alembic.ini

3. **OTP verification failed**
   - Ensure time synchronization is correct
   - Check if OTP key was generated correctly

4. **Port already in use**
```bash
# Check port usage
lsof -i :8000
lsof -i :3306
lsof -i :6379

# Stop conflicting services
docker-compose down
```

## 🗂 Environment Configuration

### Local Development Environment

- Database: `mysql+pymysql://root:root@localhost/sso-fastapi`
- Redis: `localhost:6379`

### Docker Environment

- Database: `mysql+pymysql://root:root@mysql/sso-fastapi`
- Redis: `redis:6379`

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

[Add your license information]

## 📞 Contact

[Add contact information]