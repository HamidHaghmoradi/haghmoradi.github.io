#!/usr/bin/env python3
"""
Simple HTTP server that supports POST requests for login form testing
"""
import http.server
import socketserver
import urllib.parse
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/edit.html'):
            # Parse the POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse form data
                parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                username = parsed_data.get('username', [''])[0]
                password = parsed_data.get('password', [''])[0]
                
                print(f"POST login attempt - Username: '{username}', Password: '{password}'")
                
                # For our purposes, we'll just redirect back to the edit page
                # The actual authentication is handled by JavaScript
                self.send_response(302)
                self.send_header('Location', '/edit.html')
                self.end_headers()
                
            except Exception as e:
                print(f"Error processing POST: {e}")
                self.send_response(400)
                self.end_headers()
        else:
            # For other POST requests, return 404
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Handle GET requests - use default behavior"""
        return super().do_GET()
    
    def end_headers(self):
        # Add CORS headers if needed
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server(port=8888):
    """Run the custom HTTP server"""
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"Server running at http://localhost:{port}/")
            print("Serving files from current directory...")
            print("Supports both GET and POST requests")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        print(f"Error starting server: {e}")
        if "Address already in use" in str(e):
            print(f"Port {port} is already in use. Try a different port.")

if __name__ == "__main__":
    import sys
    port = 8888
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8888.")
    
    run_server(port)
