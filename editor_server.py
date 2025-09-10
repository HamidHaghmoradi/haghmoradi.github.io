#!/usr/bin/env python3
"""
Advanced Website Editor Server
Handles both serving the website and saving edits back to files
"""

import http.server
import socketserver
import json
import os
import urllib.parse
import cgi
import io
from pathlib import Path
import logging
import shutil
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebsiteEditorHandler(http.server.SimpleHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        # Log the request
        logging.info(f"GET request: {self.path}")
        
        # Serve files normally
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for saving edits"""
        try:
            logging.info(f"POST request: {self.path}")
            
            # Parse the URL
            parsed_path = urllib.parse.urlparse(self.path)
            
            if parsed_path.path == '/save-website':
                self.handle_save_website()
            elif parsed_path.path == '/save-image':
                self.handle_save_image()
            elif parsed_path.path == '/backup-website':
                self.handle_backup_website()
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            logging.error(f"Error handling POST request: {e}")
            self.send_error(500, f"Server error: {str(e)}")
    
    def handle_save_website(self):
        """Save the edited website content back to index.html"""
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            
            # Read the POST data
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            html_content = data.get('html', '')
            backup = data.get('backup', True)
            
            if not html_content:
                self.send_json_response({'success': False, 'error': 'No HTML content provided'})
                return
            
            # Create backup if requested
            if backup:
                self.create_backup()
            
            # Clean the HTML content (remove editor toolbar and scripts)
            cleaned_html = self.clean_html_content(html_content)
            
            # Save to index.html
            index_path = Path('index.html')
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_html)
            
            logging.info("Website content saved successfully to index.html")
            
            self.send_json_response({
                'success': True, 
                'message': 'Website saved successfully!',
                'timestamp': datetime.now().isoformat()
            })
            
        except json.JSONDecodeError:
            self.send_json_response({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            logging.error(f"Error saving website: {e}")
            self.send_json_response({'success': False, 'error': str(e)})
    
    def handle_save_image(self):
        """Handle image uploads and replacements"""
        try:
            # Parse multipart form data
            content_type = self.headers['Content-Type']
            if not content_type.startswith('multipart/form-data'):
                self.send_json_response({'success': False, 'error': 'Invalid content type'})
                return
            
            # Parse the form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            image_file = form['image']
            filename = form.getvalue('filename', 'uploaded_image.jpg')
            
            if not image_file.file:
                self.send_json_response({'success': False, 'error': 'No image file provided'})
                return
            
            # Ensure images directory exists
            images_dir = Path('images')
            images_dir.mkdir(exist_ok=True)
            
            # Save the image
            image_path = images_dir / filename
            with open(image_path, 'wb') as f:
                shutil.copyfileobj(image_file.file, f)
            
            logging.info(f"Image saved: {image_path}")
            
            self.send_json_response({
                'success': True,
                'message': f'Image {filename} saved successfully!',
                'path': f'images/{filename}'
            })
            
        except Exception as e:
            logging.error(f"Error saving image: {e}")
            self.send_json_response({'success': False, 'error': str(e)})
    
    def handle_backup_website(self):
        """Create a backup of the current website"""
        try:
            backup_path = self.create_backup()
            self.send_json_response({
                'success': True,
                'message': f'Backup created: {backup_path}',
                'backup_path': str(backup_path)
            })
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            self.send_json_response({'success': False, 'error': str(e)})
    
    def create_backup(self):
        """Create a timestamped backup of index.html"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = Path(f'backups/index_backup_{timestamp}.html')
        
        # Ensure backups directory exists
        backup_path.parent.mkdir(exist_ok=True)
        
        # Copy current index.html to backup
        if Path('index.html').exists():
            shutil.copy2('index.html', backup_path)
            logging.info(f"Backup created: {backup_path}")
        
        return backup_path
    
    def clean_html_content(self, html_content):
        """Remove editor-specific elements from HTML before saving"""
        import re
        
        # First, extract the original website content from inside the editor
        # Look for the content after the toolbar
        content_match = re.search(r'<!-- Your Original Website Content -->(.*?)</body>', html_content, re.DOTALL)
        
        if content_match:
            # Get just the website content
            website_content = content_match.group(1)
            
            # Clean ALL inline styles that contain animation properties
            website_content = re.sub(r'\s*style="[^"]*"', '', website_content)
            
            # Reconstruct the original HTML structure
            clean_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hamid Haghmoradi | Quantum Force Metrology</title>
    <meta name="description" content="Doctoral Researcher in Quantum Force Metrology">
    
    <!-- Enhanced Favicon Support -->
    <link rel="icon" type="image/svg+xml" href="images/favicon.svg">
    <link rel="icon" type="image/svg+xml" sizes="32x32" href="images/favicon.svg">
    <link rel="icon" type="image/svg+xml" sizes="16x16" href="images/favicon-16x16.svg">
    <link rel="alternate icon" href="images/favicon.svg">
    <link rel="mask-icon" href="images/favicon.svg" color="#007AFF">
    <link rel="apple-touch-icon" href="images/favicon.svg">
    <meta name="theme-color" content="#007AFF">
    <meta name="msapplication-TileColor" content="#007AFF">
    <meta name="msapplication-TileImage" content="images/favicon.svg">
    <link rel="manifest" href="manifest.json">
    
    <link rel="stylesheet" href="styles/main.css">
    <link rel="stylesheet" href="fix.css?v=2.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="custom_editor_styles.css">
</head>
<body>''' + website_content + '''

    <script src="scripts/main.js"></script>
</body>
</html>'''
            
            # Clean up editor-specific content
            clean_html = re.sub(r'\s*contenteditable="[^"]*"', '', clean_html)
            clean_html = re.sub(r'\s*class="editing-mode"', '', clean_html)
            clean_html = re.sub(r'\s*class="img-selected"', '', clean_html)
            clean_html = re.sub(r'<div class="img-wrapper"[^>]*>', '', clean_html)
            clean_html = re.sub(r'<div class="img-controls">.*?</div>', '', clean_html, flags=re.DOTALL)
            
            # Remove extra closing divs that were added by image wrappers
            clean_html = re.sub(r'</div>\s*(?=<script|</body)', '', clean_html)
            
            return clean_html
        
        # Fallback: try to clean the full HTML if structure not found
        html_content = re.sub(r'<div class="editor-toolbar">.*?</div>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<div class="upload-overlay".*?</div>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<input[^>]*id="imageUpload"[^>]*>', '', html_content)
        html_content = re.sub(r'<script>.*?console\.log\(.*?Live Website Editor.*?\);.*?</script>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<!-- Editor overlay styles -->.*?</style>', '', html_content, flags=re.DOTALL)
        html_content = re.sub(r'padding-top:\s*60px;?', '', html_content)
        html_content = re.sub(r'\s*class="editing-mode"', '', html_content)
        html_content = re.sub(r'\s*contenteditable="[^"]*"', '', html_content)
        html_content = re.sub(r'\s*class="img-selected"', '', html_content)
        html_content = re.sub(r'<div class="img-wrapper"[^>]*>', '', html_content)
        html_content = re.sub(r'<div class="img-controls">.*?</div>', '', html_content, flags=re.DOTALL)
        
        # Clean ALL inline styles
        html_content = re.sub(r'\s*style="[^"]*"', '', html_content)
        
        return html_content
    
    def send_json_response(self, data):
        """Send a JSON response"""
        json_data = json.dumps(data).encode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_data))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(json_data)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    PORT = 8888
    
    print(f"🚀 Advanced Website Editor Server")
    print(f"📁 Serving from: {os.getcwd()}")
    print(f"🌐 Server running at: http://localhost:{PORT}/")
    print(f"✏️ Editor access: http://localhost:{PORT}/edit.html")
    print(f"💾 Supports live editing with file saving")
    print(f"📋 Features: Save to files, image uploads, automatic backups")
    print(f"🔧 Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), WebsiteEditorHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()
