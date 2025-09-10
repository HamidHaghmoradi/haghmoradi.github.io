# Website Editor Setup Instructions

## 🔐 Secure Admin Access Setup

Your website now has a secure admin panel with the following features:

### 🌐 Access Routes
- **Main Website**: `haghmoradi.com`
- **Admin Login**: `haghmoradi.com/edit`
- **Editor Interface**: `haghmoradi.com/editor` (protected)

### 🔑 Default Credentials
- **Username**: `admin`
- **Password**: `admin`

⚠️ **IMPORTANT**: Change these credentials immediately after first login!

### 🛡️ Security Features
- ✅ **Session-based authentication** (30-minute timeout)
- ✅ **Failed attempt tracking** (5 attempts before lockout)
- ✅ **IP-based lockout** (5 minutes after max attempts)
- ✅ **Access logging** (all attempts logged)
- ✅ **Session timeout protection**
- ✅ **CSRF protection** via Flask sessions
- ✅ **Security headers** (XSS, Content-Type, Frame protection)

### 🚀 Local Testing
```bash
# Install dependencies
pip3 install Flask

# Start secure server
python3 secure_server.py

# Access admin panel
http://localhost:5555/edit
```

### 📦 Production Deployment

For production deployment on haghmoradi.com:

1. **Upload all files** to your web server
2. **Configure web server** to run the Flask application
3. **Set up HTTPS** (required for production)
4. **Change default credentials** immediately
5. **Configure environment variables** for production secrets

### 🔧 Web Server Configuration

#### Apache (.htaccess)
```apache
RewriteEngine On
RewriteRule ^edit$ /secure_server.py [L,QSA]
RewriteRule ^editor$ /secure_server.py [L,QSA]
```

#### Nginx
```nginx
location /edit {
    proxy_pass http://127.0.0.1:5555/edit;
}
location /editor {
    proxy_pass http://127.0.0.1:5555/editor;
}
```

### 🔐 Password Change Process

1. Login with default credentials
2. Access editor interface
3. Use the password change API endpoint
4. Or modify the `secure_server.py` file directly

### 📊 Access Logs

The system automatically logs:
- Login attempts (success/failure)
- IP addresses
- Timestamps
- User agents
- Password changes

### 🎨 Editor Features

Once authenticated, you have full control over:
- **Website colors** (primary, secondary, accent)
- **Logo size and positioning**
- **Content editing** (titles, descriptions)
- **Real-time preview**
- **Configuration export**

### 🔄 Session Management

- Sessions expire after 30 minutes of inactivity
- Manual logout available in editor
- Automatic session renewal on activity
- Secure session storage

### 🛠️ Customization

To modify authentication:
1. Edit `secure_server.py`
2. Update `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH`
3. Adjust `SESSION_TIMEOUT`, `MAX_LOGIN_ATTEMPTS`, `LOCKOUT_TIME`
4. Restart server

### 🌟 Usage Workflow

1. **Visit**: `haghmoradi.com/edit`
2. **Login**: Enter admin credentials
3. **Edit**: Use visual editor interface
4. **Preview**: See changes in real-time
5. **Export**: Save configuration
6. **Logout**: Secure session termination

Your website is now professionally secured with enterprise-level authentication! 🎉
