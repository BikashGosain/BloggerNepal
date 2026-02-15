# 🐳 BloggerNepal - Docker Setup Guide

## 📋 Prerequisites

- Docker Desktop installed
  - [Windows/Mac Download](https://www.docker.com/products/docker-desktop)
  - Linux: `sudo apt-get install docker.io docker-compose`

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/BikashGosain/BloggerNepal.git
cd blog_main
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env with your credentials (optional for basic testing)
```

### 3. Start Docker
```bash
docker-compose up -d
```

### 4. Initialize Database
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. Access Application

- **HTTPS:** https://localhost
- **HTTP:** http://localhost
- **Admin:** https://localhost/admin

## 🛠️ Common Commands
```bash
# View logs
docker-compose logs -f web

# Stop
docker-compose down

# Restart
docker-compose restart
```

## 📝 Full Documentation

See [README.md](README.md) for complete setup instructions.
