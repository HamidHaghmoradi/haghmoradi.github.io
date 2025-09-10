#!/usr/bin/env python3
"""
Secure Website Editor Server
Handles authentication and routing for the website editor
"""

from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate secure secret key

# Configuration
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('admin')  # Will be changed later
SESSION_TIMEOUT = timedelta(minutes=30)
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME = timedelta(minutes=5)

# In-memory storage (in production, use a database)
failed_attempts = {}
lockouts = {}
access_logs = []

def log_access(ip, username, success, user_agent):
    """Log access attempts"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'ip': ip,
        'username': username,
        'success': success,
        'user_agent': user_agent
    }
    access_logs.append(log_entry)
    
    # Keep only last 1000 entries
    if len(access_logs) > 1000:
        access_logs.pop(0)
    
    print(f"Access attempt: {log_entry}")

def is_locked_out(ip):
    """Check if IP is locked out"""
    if ip in lockouts:
        if datetime.now() < lockouts[ip]:
            return True
        else:
            # Lockout expired
            del lockouts[ip]
            if ip in failed_attempts:
                del failed_attempts[ip]
    return False

def check_auth():
    """Check if user is authenticated"""
    if 'authenticated' not in session:
        return False
    
    if 'auth_time' not in session:
        return False
    
    # Check session timeout
    auth_time = datetime.fromisoformat(session['auth_time'])
    if datetime.now() - auth_time > SESSION_TIMEOUT:
        session.clear()
        return False
    
    # Update auth time
    session['auth_time'] = datetime.now().isoformat()
    return True

@app.route('/')
def index():
    """Serve main website"""
    return send_from_directory('.', 'index.html')

@app.route('/edit')
def admin_login():
    """Admin login page"""
    # If already authenticated, redirect to editor
    if check_auth():
        return redirect('/editor')
    
    return send_from_directory('.', 'edit.html')

@app.route('/editor')
def editor():
    """Protected editor page"""
    if not check_auth():
        return redirect('/edit')
    
    return send_from_directory('.', 'editor.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Handle login authentication"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    
    # Check if IP is locked out
    if is_locked_out(ip):
        log_access(ip, username, False, user_agent)
        return jsonify({
            'success': False,
            'message': 'IP address temporarily locked due to too many failed attempts'
        }), 429
    
    # Validate credentials
    if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
        # Successful login
        session['authenticated'] = True
        session['auth_time'] = datetime.now().isoformat()
        session['username'] = username
        
        # Clear failed attempts for this IP
        if ip in failed_attempts:
            del failed_attempts[ip]
        
        log_access(ip, username, True, user_agent)
        
        return jsonify({
            'success': True,
            'message': 'Authentication successful'
        })
    else:
        # Failed login
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
        
        if failed_attempts[ip] >= MAX_LOGIN_ATTEMPTS:
            # Lock out IP
            lockouts[ip] = datetime.now() + LOCKOUT_TIME
            
        log_access(ip, username, False, user_agent)
        
        remaining = max(0, MAX_LOGIN_ATTEMPTS - failed_attempts[ip])
        
        return jsonify({
            'success': False,
            'message': f'Invalid credentials. {remaining} attempts remaining.',
            'attempts_remaining': remaining
        }), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/check-auth', methods=['GET'])
def check_authentication():
    """Check authentication status"""
    return jsonify({'authenticated': check_auth()})

@app.route('/api/update-website', methods=['POST'])
def update_website():
    """Update website configuration (protected endpoint)"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        # Here you would update the actual website files
        # For now, just save the configuration
        config_file = 'website_config.json'
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Website updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating website: {str(e)}'
        }), 500

@app.route('/api/logs')
def get_logs():
    """Get access logs (protected endpoint)"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    return jsonify({
        'logs': access_logs[-50:],  # Last 50 entries
        'total': len(access_logs)
    })

@app.route('/api/change-password', methods=['POST'])
def change_password():
    """Change admin password (protected endpoint)"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    
    global ADMIN_PASSWORD_HASH
    
    if not check_password_hash(ADMIN_PASSWORD_HASH, current_password):
        return jsonify({
            'success': False,
            'message': 'Current password is incorrect'
        }), 401
    
    if len(new_password) < 8:
        return jsonify({
            'success': False,
            'message': 'New password must be at least 8 characters long'
        }), 400
    
    ADMIN_PASSWORD_HASH = generate_password_hash(new_password)
    
    log_access(request.remote_addr, session.get('username'), True, 
               request.headers.get('User-Agent', '') + ' - Password Changed')
    
    return jsonify({
        'success': True,
        'message': 'Password changed successfully'
    })

# Serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

# Security headers
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    print("🚀 Starting Secure Website Editor Server...")
    print("📍 Admin access: http://localhost:5555/edit")
    print("🔐 Default credentials: admin / admin")
    print("⚠️  Change default password after first login!")
    print()
    
    app.run(host='0.0.0.0', port=5555, debug=False)
