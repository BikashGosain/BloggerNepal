# BloggerNepal 🇳🇵
## Live Demo

Check out the live application here: [Live Demo](https://web-based-blogging-platform-with-content.onrender.com)

A community-focused blogging platform designed especially for Nepali audiences, built with Django.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 About The Project

BloggerNepal is a community-focused blogging platform designed to provide a simple and easy blogging system where users, especially beginners, can create, manage, and interact with blogs without technical complexity.

Unlike other platforms, BloggerNepal emphasizes **community interaction**. Users can not only publish their own blogs but also follow other authors, like posts, and comment to encourage engagement among writers.

### Why BloggerNepal?

- **🎯 Local Focus**: Built specifically for Nepali creators and audiences
- **🆓 Free & Open**: All blogs freely accessible without login or paywalls
- **👥 Community-Driven**: Follow authors, like posts, engage through comments
- **🎨 User-Friendly**: Modern, intuitive interface for beginners
- **🔒 Full Control**: Role-based access with complete data ownership
- **✨ Authentic Content**: Real human experiences, not AI-generated content

## 🚀 Key Features

### 1. Authentication System
Secure, OTP-based authentication with third-party login options:
- **OTP-based Registration**: Email verification for secure sign-ups
- **OTP Login**: Two-factor authentication for enhanced security
- **Password Recovery**: OTP-verified password reset
- **Social Authentication**: Sign in with Google and GitHub

### 2. Role-Based Access Control (RBAC)
Multi-level user management system:
- **Guest User** - Browse content without login
- **Registered Users** - Create and manage blogs
  - Super User (Full admin access)
  - Manager (Content moderation)
  - Editor (Editorial permissions)
  - Normal Author (Standard user)

### 3. Advanced User Management
- Add, edit, and delete users
- Assign and manage user roles
- Ban/unban users
- User switching for administrative purposes
- Profile management (public/private)

### 4. Content Management (CRUD)
Comprehensive CRUD operations for:
- Blog posts (popular, recent, newest, featured)
- Categories
- Users
- Comments
- Social links
- About Us section
- Notifications

### 5. Rich Content Creation
- **Rich Text Editor** for formatted blog content
- **Image Upload** support
- **Draft & Publish** workflow
- **Automatic SEO-friendly URLs** (slug generation)
- **View Tracking** (session-based, unique views)

### 6. Community Features

#### Follow System
- Follow/unfollow authors
- View follower and following counts
- Discover content from followed authors

#### Interaction System
- Like and dislike blog posts
- **Advanced Comment System**:
  - Nested comments (threaded discussions)
  - Like/dislike on comments (planned)
  - Real-time comment updates

### 7. Advanced Notification System
- View all notifications
- Filter (All / Read / Unread)
- Mark as read / Mark all as read
- Delete individual or all notifications
- Click-to-open related blog post

### 8. Search, Filter & Sorting

#### Public Side
Search blog posts by:
- Title
- Description
- Content
- Category
- Author

#### Dashboard Side
- **Users**: Search by username, filter by roles, sort by login time
- **Categories**: Search by name
- **Posts**: Search and filter by category/author
- **Followers/Following**: Search by username

### 9. Analytics & Visualization
- **Charts**:
  - Posts per month (bar chart)
  - Category-wise distribution (bar chart)
- **Statistics**:
  - Total posts, categories, views
  - Likes, comments counts
  - Follower/following metrics

### 10. Reporting & Moderation
- Report inappropriate blog posts
- Ban, unban, or delete reported content
- User moderation controls
- Content review dashboard

### 11. Contact & Feedback
- SMTP-based contact form
- Open to all users (logged in or guest)
- Admin email reply functionality
- Query and feedback management

### 12. Dashboard System
- **Role-specific dashboards**
- Integrated analytics
- User management access by role
- Admin panel with limited permissions for managers

### 13. Pagination System
Implemented across:
- Blog post listings
- Random blogs
- Dashboard user lists
- Categories and followers lists
- All large datasets

### 14. Smart Algorithms

**Implemented:**
- Similar Posts (content-based similarity)

**Planned:**
- Recent Posts (time-based sorting)
- Category-based filtering
- Most Viewed Posts (ranking algorithm)

## 🛠️ Built With

- **Backend**: Python 3.8+, Django 4.0+
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite3 (PostgreSQL planned for production)
- **Authentication**: Django Auth + Social Auth
- **Email**: SMTP integration

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git

## 💻 Installation

**Option 1**
### 🐳 Recommended: Docker Setup (No Version Conflicts!)

The easiest way to run BloggerNepal without any dependency or version issues:
```bash
git clone https://github.com/BikashGosain/BloggerNepal.git
cd BloggerNepal
cp .env.example .env
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

**Access:** https://localhost

📖 **Detailed Docker instructions:** [SETUP.md](SETUP.md)

---

**Option 2**

### 🐍 Alternative: Manual Installation (Traditional Method)

If you prefer to run without Docker:

**Prerequisites:**
- Python 3.8+
- PostgreSQL (optional, SQLite works too)

**Steps:**

1. **Clone the repository**
   ```bash
   git clone https://github.com/BikashGosain/Web-Based-Blogging-Platform-with-Content-Recommendation-and-Analytics.git
   cd Blog
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file in project root
   cp .env.example .env
   
   # Edit .env with your settings:
   # - SECRET_KEY
   # - EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
   # - GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
   # - GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Frontend: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure
```
BloggerNepal/
│
├── 🐳 Docker Files
│   ├── Dockerfile                    # Django container definition
│   ├── docker-compose.yml            # Services orchestration (PostgreSQL, Django, Nginx)
│   ├── .dockerignore                 # Files excluded from Docker build
│   └── nginx/                        # Nginx web server configuration
│       ├── nginx.conf                # Nginx settings (HTTPS, reverse proxy)
│       ├── cert.pem                  # SSL certificate (auto-generated, not in repo)
│       └── key.pem                   # SSL private key (auto-generated, not in repo)
│
├── 📱 Django Apps
│   ├── about_us/                     # About Us page app
│   ├── blog_main/                    # Main Django project configuration
│   │   ├── settings.py               # Project settings (database, apps, middleware)
│   │   ├── urls.py                   # URL routing
│   │   ├── wsgi.py                   # WSGI config for deployment
│   │   ├── asgi.py                   # ASGI config for async
│   │   ├── adapters.py               # Social authentication adapters
│   │   ├── forms.py                  # Global forms
│   │   └── static/                   # Project-level static files
│   ├── blogs/                        # Core blogging functionality
│   ├── contact/                      # Contact form & feedback system
│   ├── dashboards/                   # Role-based admin dashboards
│   ├── follow_following/             # User follow/unfollow system
│   └── social_links/                 # Social media links management
│
├── 🎨 Frontend
│   ├── templates/                    # Global HTML templates
│   │   ├── base.html                 # Base template
│   │   ├── navbar.html               # Navigation bar
│   │   └── ...
│   ├── staticfiles/                  # Collected static files (not in repo)
│   └── media/                        # User uploads (images, etc., not in repo)
│
├── 📝 Configuration Files
│   ├── .env                          # Environment variables (SECRETS - not in repo)
│   ├── .env.example                  # Environment template (safe to share)
│   ├── .gitignore                    # Git ignore rules
│   ├── requirements.txt              # Python dependencies
│   ├── manage.py                     # Django CLI tool
│   ├── build.sh                      # Build script
│   └── start.sh                      # Startup script
│
├── 🔧 Utility Scripts
│   ├── create_groups_on_startup.py   # Auto-create user groups
│   └── create_superuser_on_startup.py # Auto-create admin user
│
└── 📚 Documentation
    ├── README.md                     # Main documentation
    └── SETUP.md                      # Docker setup guide
```

### 🔑 Key Directories Explained

| Directory | Purpose | In Git? |
|-----------|---------|---------|
| `nginx/` | Web server config with HTTPS | ✅ Config only |
| `blog_main/` | Django project settings | ✅ Yes |
| `blogs/` | Blog post CRUD operations | ✅ Yes |
| `dashboards/` | Admin & manager dashboards | ✅ Yes |
| `staticfiles/` | Compiled static assets | ❌ Generated |
| `media/` | User uploaded files | ❌ User content |
| `.env` | Secret credentials | ❌ **NEVER!** |
| `postgres_data/` | Database files (Docker) | ❌ Docker volume |

### 📦 Important Files

- **`Dockerfile`** - Defines Django container (Python, dependencies, app)
- **`docker-compose.yml`** - Orchestrates 3 services: PostgreSQL + Django + Nginx
- **`requirements.txt`** - All Python packages (Django, PostgreSQL driver, etc.)
- **`.env.example`** - Template for environment variables (safe to share)
- **`.env`** - Your actual secrets (database passwords, API keys - **never commit!**)

  
## 🎯 Future Enhancements

### Planned Features
- **Soft Delete & Restore**: Recover deleted posts and users
- **Bookmark System**: Save posts to read later
- **Advanced Algorithms**: 
  - Smart content recommendations
  - Trending posts detection
  - Personalized feed
- **PostgreSQL Migration**: Production-ready database
- **Performance Optimization**: Caching and query optimization
- **Mobile App**: Native mobile experience
- **Monetization**: Creator revenue sharing options

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 👨‍💻 Author

**Bikash Gosain**

- GitHub: [@BikashGosain](https://github.com/BikashGosain)
- Email: bikashgosain0@gmail.com

## 🙏 Acknowledgments

- Built as a BSc CSIT 7th Semester project
- Inspired by 2+ years of personal blogging experience
- Created to address limitations in existing Nepali blogging platforms
- Designed to complement AI tools with authentic human content

## 📞 Contact & Support

For questions, feedback, or support:
- Open an issue on GitHub
- Use the contact form on the platform
- Email: bikashgosain@gamil.com

---

**Note**: This project is designed specifically for the Nepali blogging community and focuses on providing authentic human content, community interaction, and local-focused features that complement rather than compete with AI tools and international platforms.

**Made with ❤️ for the Nepali blogging community**
