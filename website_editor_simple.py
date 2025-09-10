#!/usr/bin/env python3
"""
Website Template Editor - Simplified Version
A comprehensive Python interface for editing website templates with real-time preview.
"""

import os
import json
import shutil
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox, scrolledtext
import webbrowser
import threading
import http.server
import socketserver
from pathlib import Path

class WebsiteEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Website Template Editor v1.0")
        self.root.geometry("1400x900")
        
        # Template configuration
        self.template_path = None
        self.config_file = "editor_config.json"
        self.preview_port = 8090
        self.server_thread = None
        
        # Website configuration data
        self.website_config = {
            "meta": {
                "title": "Hamid Haghmoradi | Quantum Force Metrology",
                "description": "Doctoral Researcher in Quantum Force Metrology",
                "author": "Hamid Haghmoradi",
                "version": "1.0.0"
            },
            "colors": {
                "primary": "#007AFF",
                "secondary": "#5856D6",
                "accent": "#FF9F0A",
                "background": "#FFFFFF",
                "text": "#000000"
            },
            "logo": {
                "src": "images/logo.svg",
                "width": "6rem",
                "height": "6rem",
                "alt": "HH Logo"
            },
            "navigation": {
                "title": "Hamid Haghmoradi",
                "menu_items": ["Home", "Research", "Publications", "Contact"]
            },
            "sections": [],
            "images": {},
            "tiles": []
        }
        
        self.setup_ui()
        self.load_template()
    
    def setup_ui(self):
        """Create the main user interface"""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Template Management Tab
        self.create_template_tab()
        
        # Content Editor Tab
        self.create_content_tab()
        
        # Design Customization Tab
        self.create_design_tab()
        
        # Image Manager Tab
        self.create_image_tab()
        
        # Preview & Export Tab
        self.create_preview_tab()
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Template", command=self.load_template_dialog)
        file_menu.add_command(label="Save Configuration", command=self.save_config)
        file_menu.add_command(label="Load Configuration", command=self.load_config)
        file_menu.add_separator()
        file_menu.add_command(label="Export Website", command=self.export_website)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Start Preview Server", command=self.start_preview_server)
        tools_menu.add_command(label="Stop Preview Server", command=self.stop_preview_server)
        tools_menu.add_command(label="Open in Browser", command=self.open_preview)
    
    def create_template_tab(self):
        """Create template management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Template")
        
        # Template selection
        ttk.Label(frame, text="Website Template Editor", font=("Arial", 18, "bold")).pack(pady=10)
        ttk.Label(frame, text="Complete control over your website design and content", font=("Arial", 12)).pack(pady=5)
        
        template_frame = ttk.LabelFrame(frame, text="Template Selection")
        template_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(template_frame, text="Load Template Folder", 
                  command=self.load_template_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.template_label = ttk.Label(template_frame, text="Current template loaded")
        self.template_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Quick start guide
        guide_frame = ttk.LabelFrame(frame, text="Quick Start Guide")
        guide_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        guide_text = """
🎨 DESIGN CUSTOMIZATION:
• Change colors using the Design tab
• Upload custom logo and adjust size
• Add custom CSS for advanced styling

📝 CONTENT MANAGEMENT:
• Edit website title and description
• Modify navigation and branding
• Add/remove/reorder content sections

🖼️ IMAGE MANAGEMENT:
• Upload new images
• Resize and position images
• Apply different frame styles

🔄 REAL-TIME PREVIEW:
• Start preview server to see changes live
• Open in browser for full testing
• Export when ready with version control

💡 TIPS:
• All changes maintain mobile compatibility
• Use web-safe colors for best results
• Export regularly to save progress
• Original template is never modified
        """
        
        guide_label = tk.Label(guide_frame, text=guide_text, justify=tk.LEFT, font=("Courier", 10))
        guide_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_content_tab(self):
        """Create content editing tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 Content")
        
        # Meta information
        meta_frame = ttk.LabelFrame(frame, text="Website Meta Information")
        meta_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Title
        ttk.Label(meta_frame, text="Website Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_var = tk.StringVar(value=self.website_config["meta"]["title"])
        title_entry = ttk.Entry(meta_frame, textvariable=self.title_var, width=70, font=("Arial", 11))
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(meta_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.desc_var = tk.StringVar(value=self.website_config["meta"]["description"])
        desc_entry = ttk.Entry(meta_frame, textvariable=self.desc_var, width=70, font=("Arial", 11))
        desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Navigation
        nav_frame = ttk.LabelFrame(frame, text="Navigation & Branding")
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(nav_frame, text="Brand Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.brand_var = tk.StringVar(value=self.website_config["navigation"]["title"])
        brand_entry = ttk.Entry(nav_frame, textvariable=self.brand_var, width=50, font=("Arial", 12, "bold"))
        brand_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Content preview
        preview_frame = ttk.LabelFrame(frame, text="Content Preview & Text Editing")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Text editor
        text_frame = ttk.Frame(preview_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(text_frame, text="Edit website content (HTML supported):", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0,5))
        
        self.content_editor = scrolledtext.ScrolledText(text_frame, height=20, width=100, font=("Courier", 10))
        self.content_editor.pack(fill=tk.BOTH, expand=True)
        
        # Load current content
        self.load_current_content()
        
        # Buttons
        button_frame = ttk.Frame(preview_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="💾 Save Changes", command=self.save_content_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Reload Content", command=self.load_current_content).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="👁️ Preview Changes", command=self.preview_content).pack(side=tk.LEFT, padx=5)
    
    def create_design_tab(self):
        """Create design customization tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎨 Design")
        
        # Color scheme
        color_frame = ttk.LabelFrame(frame, text="Color Scheme Customization")
        color_frame.pack(fill=tk.X, padx=10, pady=5)
        
        colors = [
            ("Primary Color (Main Brand)", "primary", "#007AFF"),
            ("Secondary Color (Accents)", "secondary", "#5856D6"),
            ("Accent Color (Highlights)", "accent", "#FF9F0A"),
            ("Background Color", "background", "#FFFFFF"),
            ("Text Color", "text", "#000000")
        ]
        
        self.color_vars = {}
        self.color_previews = {}
        
        for i, (label, key, default) in enumerate(colors):
            ttk.Label(color_frame, text=label + ":", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            color_var = tk.StringVar(value=self.website_config["colors"][key])
            self.color_vars[key] = color_var
            
            # Color preview frame
            preview_frame = tk.Frame(color_frame, width=30, height=20, bg=color_var.get())
            preview_frame.grid(row=i, column=1, padx=5, pady=5)
            self.color_previews[key] = preview_frame
            
            color_entry = ttk.Entry(color_frame, textvariable=color_var, width=12, font=("Courier", 10))
            color_entry.grid(row=i, column=2, padx=5, pady=5)
            
            ttk.Button(color_frame, text="Choose Color", 
                      command=lambda k=key: self.choose_color(k)).grid(row=i, column=3, padx=5, pady=5)
            
            # Update preview when color changes
            color_var.trace('w', lambda *args, k=key: self.update_color_preview(k))
        
        # Logo settings
        logo_frame = ttk.LabelFrame(frame, text="Logo Configuration")
        logo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(logo_frame, text="Logo File:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.logo_src_var = tk.StringVar(value=self.website_config["logo"]["src"])
        ttk.Entry(logo_frame, textvariable=self.logo_src_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(logo_frame, text="Browse & Upload", command=self.browse_logo).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(logo_frame, text="Width:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.logo_width_var = tk.StringVar(value=self.website_config["logo"]["width"])
        width_frame = ttk.Frame(logo_frame)
        width_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(width_frame, textvariable=self.logo_width_var, width=10).pack(side=tk.LEFT)
        ttk.Label(width_frame, text="(e.g., 6rem, 100px, auto)").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(logo_frame, text="Height:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.logo_height_var = tk.StringVar(value=self.website_config["logo"]["height"])
        height_frame = ttk.Frame(logo_frame)
        height_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(height_frame, textvariable=self.logo_height_var, width=10).pack(side=tk.LEFT)
        ttk.Label(height_frame, text="(e.g., 6rem, 100px, auto)").pack(side=tk.LEFT, padx=5)
        
        # CSS customization
        css_frame = ttk.LabelFrame(frame, text="Advanced CSS Customization")
        css_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(css_frame, text="Custom CSS (for advanced users):", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        
        self.custom_css = scrolledtext.ScrolledText(css_frame, height=15, width=100, font=("Courier", 10))
        self.custom_css.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add some example CSS
        example_css = """/* Example custom CSS - modify as needed */

/* Custom button styling */
.custom-button {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    color: white;
    font-weight: bold;
    transition: all 0.3s ease;
}

.custom-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Custom section styling */
.custom-section {
    background: linear-gradient(135deg, #f8f9fa, #ffffff);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}
"""
        self.custom_css.insert(1.0, example_css)
    
    def create_image_tab(self):
        """Create image management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🖼️ Images")
        
        # Instructions
        instructions = ttk.LabelFrame(frame, text="Image Management Guide")
        instructions.pack(fill=tk.X, padx=10, pady=5)
        
        guide_text = """
📸 Upload images → 🎨 Customize properties → 📱 Auto-responsive optimization → 🌐 Use in website

Supported formats: JPG, PNG, SVG, GIF, WebP | Frame styles: None, Rounded, Circle, Shadow, Border
        """
        ttk.Label(instructions, text=guide_text, font=("Arial", 10)).pack(padx=10, pady=5)
        
        # Main container
        main_container = ttk.Frame(frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - Image list
        left_frame = ttk.LabelFrame(main_container, text="Image Gallery")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Image listbox with scrollbar
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_listbox = tk.Listbox(list_container, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Image controls
        controls_frame = ttk.Frame(left_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="📁 Add Images", command=self.add_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="🗑️ Remove", command=self.remove_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="⚙️ Properties", command=self.edit_image_properties).pack(side=tk.LEFT, padx=2)
        
        # Right side - Properties
        right_frame = ttk.LabelFrame(main_container, text="Image Properties")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Image preview placeholder
        self.image_preview_label = ttk.Label(right_frame, text="Select an image\\nto view properties", 
                                           font=("Arial", 11), justify=tk.CENTER)
        self.image_preview_label.pack(pady=20)
        
        # Properties form
        props_frame = ttk.Frame(right_frame)
        props_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Current properties display
        self.props_text = scrolledtext.ScrolledText(props_frame, width=30, height=15, font=("Arial", 9))
        self.props_text.pack(fill=tk.BOTH, expand=True)
        
        self.image_listbox.bind('<<ListboxSelect>>', self.on_image_select)
    
    def create_preview_tab(self):
        """Create preview and export tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔄 Preview & Export")
        
        # Preview controls
        preview_controls = ttk.LabelFrame(frame, text="Live Preview System")
        preview_controls.pack(fill=tk.X, padx=10, pady=5)
        
        control_buttons = ttk.Frame(preview_controls)
        control_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_buttons, text="🚀 Start Preview Server", 
                  command=self.start_preview_server).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_buttons, text="🔄 Generate Preview", 
                  command=self.generate_preview).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_buttons, text="🌐 Open in Browser", 
                  command=self.open_preview).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_buttons, text="🛑 Stop Server", 
                  command=self.stop_preview_server).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Preview status
        self.preview_status = ttk.Label(preview_controls, text="Preview server stopped", 
                                       font=("Arial", 11, "bold"), foreground="red")
        self.preview_status.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Export controls
        export_frame = ttk.LabelFrame(frame, text="Version Control & Export")
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        export_controls = ttk.Frame(export_frame)
        export_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(export_controls, text="Version Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.version_var = tk.StringVar(value="v1.1")
        version_entry = ttk.Entry(export_controls, textvariable=self.version_var, width=15, font=("Arial", 11))
        version_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(export_controls, text="📦 Export Website", 
                  command=self.export_website).grid(row=0, column=2, padx=10, pady=5)
        
        # Current stats
        stats_frame = ttk.Frame(export_frame)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="Ready to export", font=("Arial", 10))
        self.stats_label.pack(side=tk.LEFT)
        
        # Export log
        log_frame = ttk.LabelFrame(frame, text="Activity Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.export_log = scrolledtext.ScrolledText(log_frame, height=20, width=100, font=("Courier", 9))
        self.export_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize log
        self.log_message("Website Template Editor initialized")
        self.log_message("Ready to load template and start editing")
    
    def load_template_dialog(self):
        """Load template from folder"""
        folder = filedialog.askdirectory(title="Select Template Folder")
        if folder:
            self.template_path = folder
            self.template_label.config(text=f"Template: {os.path.basename(folder)}")
            self.analyze_template()
            self.log_message(f"Template loaded: {folder}")
    
    def load_template(self):
        """Load current template"""
        if not self.template_path:
            self.template_path = os.path.dirname(os.path.abspath(__file__))
            self.template_label.config(text=f"Template: {os.path.basename(self.template_path)}")
        self.analyze_template()
    
    def analyze_template(self):
        """Analyze template structure"""
        if not self.template_path:
            return
        
        # Find and load current images
        image_files = []
        for root, dirs, files in os.walk(self.template_path):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.template_path)
                    image_files.append(rel_path)
        
        self.update_image_list(image_files)
        self.log_message(f"Found {len(image_files)} images in template")
    
    def update_image_list(self, image_files):
        """Update image listbox"""
        self.image_listbox.delete(0, tk.END)
        for image_file in image_files:
            self.image_listbox.insert(tk.END, image_file)
    
    def update_color_preview(self, color_key):
        """Update color preview frame"""
        try:
            color = self.color_vars[color_key].get()
            if color and color.startswith('#') and len(color) == 7:
                self.color_previews[color_key].config(bg=color)
        except:
            pass
    
    def choose_color(self, color_key):
        """Open color chooser"""
        color = colorchooser.askcolor(color=self.color_vars[color_key].get())[1]
        if color:
            self.color_vars[color_key].set(color)
            self.update_color_preview(color_key)
            self.log_message(f"Updated {color_key} color to {color}")
    
    def browse_logo(self):
        """Browse for logo file"""
        file_path = filedialog.askopenfilename(
            title="Select Logo File",
            filetypes=[
                ("SVG files", "*.svg"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("All images", "*.svg;*.png;*.jpg;*.jpeg;*.gif")
            ]
        )
        if file_path and self.template_path:
            # Copy to template directory
            images_dir = os.path.join(self.template_path, 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            dest_path = os.path.join(images_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)
            
            rel_path = f"images/{os.path.basename(file_path)}"
            self.logo_src_var.set(rel_path)
            
            self.log_message(f"Logo uploaded: {rel_path}")
            self.analyze_template()  # Refresh image list
    
    def load_current_content(self):
        """Load current HTML content for editing"""
        if not self.template_path:
            return
        
        html_file = os.path.join(self.template_path, "index.html")
        if os.path.exists(html_file):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.content_editor.delete(1.0, tk.END)
                self.content_editor.insert(1.0, content)
                self.log_message("Current content loaded for editing")
            except Exception as e:
                self.log_message(f"Error loading content: {e}")
    
    def save_content_changes(self):
        """Save content changes to HTML file"""
        if not self.template_path:
            messagebox.showerror("Error", "No template loaded")
            return
        
        try:
            content = self.content_editor.get(1.0, tk.END)
            
            html_file = os.path.join(self.template_path, "index.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log_message("Content changes saved successfully")
            messagebox.showinfo("Success", "Content saved successfully!")
        except Exception as e:
            self.log_message(f"Error saving content: {e}")
            messagebox.showerror("Error", f"Could not save content: {e}")
    
    def preview_content(self):
        """Preview content changes"""
        self.save_content_changes()
        self.generate_preview()
        self.open_preview()
    
    def add_image(self):
        """Add new image"""
        file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.svg;*.webp"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("PNG files", "*.png"),
                ("SVG files", "*.svg"),
                ("All files", "*.*")
            ]
        )
        
        if file_paths and self.template_path:
            images_dir = os.path.join(self.template_path, 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            added_count = 0
            for file_path in file_paths:
                try:
                    dest_path = os.path.join(images_dir, os.path.basename(file_path))
                    shutil.copy2(file_path, dest_path)
                    
                    rel_path = f"images/{os.path.basename(file_path)}"
                    self.image_listbox.insert(tk.END, rel_path)
                    added_count += 1
                except Exception as e:
                    self.log_message(f"Error adding {file_path}: {e}")
            
            self.log_message(f"Added {added_count} images to gallery")
            if added_count > 0:
                messagebox.showinfo("Success", f"Added {added_count} images successfully!")
    
    def remove_image(self):
        """Remove selected image"""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            image_path = self.image_listbox.get(index)
            
            if messagebox.askyesno("Confirm Delete", f"Delete {os.path.basename(image_path)}?"):
                full_path = os.path.join(self.template_path, image_path)
                try:
                    os.remove(full_path)
                    self.image_listbox.delete(index)
                    self.log_message(f"Removed image: {image_path}")
                    messagebox.showinfo("Success", "Image removed successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file: {e}")
    
    def edit_image_properties(self):
        """Edit image properties"""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            image_path = self.image_listbox.get(index)
            self.image_properties_dialog(image_path)
        else:
            messagebox.showwarning("No Selection", "Please select an image first")
    
    def image_properties_dialog(self, image_path):
        """Open image properties dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Image Properties - {os.path.basename(image_path)}")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        # Current properties
        current_props = self.website_config["images"].get(image_path, {
            "alt": os.path.splitext(os.path.basename(image_path))[0],
            "width": "auto",
            "height": "auto",
            "frame": "none",
            "position": "center"
        })
        
        # Create form
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Image info
        ttk.Label(main_frame, text=f"Configuring: {image_path}", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Properties frame
        props_frame = ttk.LabelFrame(main_frame, text="Image Properties")
        props_frame.pack(fill=tk.X, pady=10)
        
        # Alt text
        ttk.Label(props_frame, text="Alt Text:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        alt_var = tk.StringVar(value=current_props.get("alt", ""))
        ttk.Entry(props_frame, textvariable=alt_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        # Dimensions
        ttk.Label(props_frame, text="Width:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        width_var = tk.StringVar(value=current_props.get("width", "auto"))
        width_frame = ttk.Frame(props_frame)
        width_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(width_frame, textvariable=width_var, width=15).pack(side=tk.LEFT)
        ttk.Label(width_frame, text="(e.g., auto, 300px, 50%)").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(props_frame, text="Height:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        height_var = tk.StringVar(value=current_props.get("height", "auto"))
        height_frame = ttk.Frame(props_frame)
        height_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(height_frame, textvariable=height_var, width=15).pack(side=tk.LEFT)
        ttk.Label(height_frame, text="(e.g., auto, 200px, 50%)").pack(side=tk.LEFT, padx=5)
        
        # Frame style
        ttk.Label(props_frame, text="Frame Style:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        frame_var = tk.StringVar(value=current_props.get("frame", "none"))
        frame_combo = ttk.Combobox(props_frame, textvariable=frame_var, 
                                  values=["none", "rounded", "circle", "shadow", "border"], width=20)
        frame_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Position
        ttk.Label(props_frame, text="Position:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        position_var = tk.StringVar(value=current_props.get("position", "center"))
        position_combo = ttk.Combobox(props_frame, textvariable=position_var, 
                                     values=["left", "center", "right", "float-left", "float-right"], width=20)
        position_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="CSS Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        preview_text = scrolledtext.ScrolledText(preview_frame, height=8, width=70, font=("Courier", 9))
        preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def update_preview():
            css_preview = f"""
/* Generated CSS for {image_path} */
img[src="{image_path}"] {{
    width: {width_var.get()};
    height: {height_var.get()};
    alt: "{alt_var.get()}";
    /* Frame: {frame_var.get()} */
    /* Position: {position_var.get()} */
}}
"""
            preview_text.delete(1.0, tk.END)
            preview_text.insert(1.0, css_preview)
        
        # Update preview on changes
        for var in [alt_var, width_var, height_var, frame_var, position_var]:
            var.trace('w', lambda *args: update_preview())
        
        update_preview()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_properties():
            self.website_config["images"][image_path] = {
                "alt": alt_var.get(),
                "width": width_var.get(),
                "height": height_var.get(),
                "frame": frame_var.get(),
                "position": position_var.get()
            }
            dialog.destroy()
            self.log_message(f"Updated properties for: {image_path}")
            self.show_image_properties(image_path)
            messagebox.showinfo("Success", "Image properties saved!")
        
        ttk.Button(button_frame, text="💾 Save Properties", command=save_properties).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def on_image_select(self, event):
        """Handle image selection"""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            image_path = self.image_listbox.get(index)
            self.show_image_properties(image_path)
    
    def show_image_properties(self, image_path):
        """Show image properties in the properties panel"""
        props = self.website_config["images"].get(image_path, {})
        
        info_text = f"""
📁 FILE: {image_path}
📏 SIZE: {props.get('width', 'auto')} x {props.get('height', 'auto')}
🖼️ FRAME: {props.get('frame', 'none')}
📍 POSITION: {props.get('position', 'center')}
🏷️ ALT TEXT: {props.get('alt', 'Not set')}

💡 USAGE EXAMPLES:
<img src="{image_path}" alt="{props.get('alt', 'image')}" 
     style="width: {props.get('width', 'auto')}; 
            height: {props.get('height', 'auto')};">

🎨 CSS CLASS SUGGESTIONS:
.image-{props.get('frame', 'default')} {{
    border-radius: {'50%' if props.get('frame') == 'circle' else '8px' if props.get('frame') == 'rounded' else '0'};
    box-shadow: {'0 4px 20px rgba(0,0,0,0.15)' if props.get('frame') == 'shadow' else 'none'};
}}
        """
        
        self.props_text.delete(1.0, tk.END)
        self.props_text.insert(1.0, info_text)
        
        # Update preview label
        self.image_preview_label.config(text=f"Selected:\\n{os.path.basename(image_path)}")
    
    def start_preview_server(self):
        """Start preview server"""
        if self.server_thread and self.server_thread.is_alive():
            self.log_message("Preview server is already running")
            return
        
        self.generate_preview()
        
        def run_server():
            try:
                os.chdir(self.template_path)
                handler = http.server.SimpleHTTPRequestHandler
                with socketserver.TCPServer(("", self.preview_port), handler) as httpd:
                    self.log_message(f"🚀 Preview server started at http://localhost:{self.preview_port}")
                    self.preview_status.config(text=f"✅ Server running on port {self.preview_port}", foreground="green")
                    httpd.serve_forever()
            except Exception as e:
                self.log_message(f"❌ Server error: {e}")
                self.preview_status.config(text="❌ Server error", foreground="red")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
    
    def stop_preview_server(self):
        """Stop preview server"""
        self.preview_status.config(text="🛑 Preview server stopped", foreground="red")
        self.log_message("🛑 Preview server stopped")
    
    def open_preview(self):
        """Open preview in browser"""
        try:
            webbrowser.open(f"http://localhost:{self.preview_port}")
            self.log_message("🌐 Opened preview in browser")
        except Exception as e:
            self.log_message(f"Error opening browser: {e}")
    
    def generate_preview(self):
        """Generate preview files"""
        if not self.template_path:
            messagebox.showerror("Error", "No template loaded")
            return
        
        try:
            self.update_config_from_ui()
            self.apply_config_to_files()
            self.log_message("✅ Preview generated successfully")
            
            # Update stats
            stats = self.get_website_stats()
            self.stats_label.config(text=stats)
            
        except Exception as e:
            self.log_message(f"❌ Error generating preview: {e}")
            messagebox.showerror("Error", f"Could not generate preview: {e}")
    
    def get_website_stats(self):
        """Get website statistics"""
        try:
            html_file = os.path.join(self.template_path, "index.html")
            if os.path.exists(html_file):
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                image_count = len([f for f in os.listdir(os.path.join(self.template_path, 'images')) 
                                 if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'))])
                
                return f"📄 HTML: {len(content)} chars | 🖼️ Images: {image_count} | 🎨 Colors: {len(self.color_vars)}"
        except:
            pass
        return "Stats unavailable"
    
    def update_config_from_ui(self):
        """Update configuration from UI elements"""
        # Meta information
        self.website_config["meta"]["title"] = self.title_var.get()
        self.website_config["meta"]["description"] = self.desc_var.get()
        
        # Navigation
        self.website_config["navigation"]["title"] = self.brand_var.get()
        
        # Colors
        for key, var in self.color_vars.items():
            self.website_config["colors"][key] = var.get()
        
        # Logo
        self.website_config["logo"]["src"] = self.logo_src_var.get()
        self.website_config["logo"]["width"] = self.logo_width_var.get()
        self.website_config["logo"]["height"] = self.logo_height_var.get()
    
    def apply_config_to_files(self):
        """Apply configuration to template files"""
        # Update HTML file
        html_file = os.path.join(self.template_path, "index.html")
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update meta information
            content = re.sub(r'<title>.*?</title>', 
                           f'<title>{self.website_config["meta"]["title"]}</title>', content)
            content = re.sub(r'<meta name="description" content=".*?"', 
                           f'<meta name="description" content="{self.website_config["meta"]["description"]}"', content)
            
            # Update logo source
            content = re.sub(r'<img src="[^"]*" alt="[^"]*" class="logo-icon">', 
                           f'<img src="{self.website_config["logo"]["src"]}" alt="{self.website_config["logo"].get("alt", "Logo")}" class="logo-icon">', content)
            
            # Update brand name
            content = re.sub(r'<span class="logo-text">.*?</span>', 
                           f'<span class="logo-text">{self.website_config["navigation"]["title"]}</span>', content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Update CSS file with custom styles
        self.update_css_file()
    
    def update_css_file(self):
        """Update CSS file with custom styles"""
        css_file = os.path.join(self.template_path, "custom_editor_styles.css")
        
        css_content = f"""
/* Generated by Website Template Editor */
/* Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} */

:root {{
    --primary-color: {self.website_config["colors"]["primary"]} !important;
    --secondary-color: {self.website_config["colors"]["secondary"]} !important;
    --accent-color: {self.website_config["colors"]["accent"]} !important;
    --background-color: {self.website_config["colors"]["background"]} !important;
    --text-color: {self.website_config["colors"]["text"]} !important;
}}

/* Logo customization */
.logo-icon,
.nav .logo-icon,
.nav-container .logo-icon,
.nav-logo .logo-icon {{
    width: {self.website_config["logo"]["width"]} !important;
    height: {self.website_config["logo"]["height"]} !important;
}}

/* Image customizations */
"""
        
        # Add image-specific CSS
        for image_path, props in self.website_config["images"].items():
            css_content += f"""
/* Styles for {image_path} */
img[src="{image_path}"] {{
    width: {props.get('width', 'auto')} !important;
    height: {props.get('height', 'auto')} !important;
"""
            
            # Add frame styles
            frame_style = props.get('frame', 'none')
            if frame_style == 'rounded':
                css_content += "    border-radius: 12px !important;\\n"
            elif frame_style == 'circle':
                css_content += "    border-radius: 50% !important;\\n"
            elif frame_style == 'shadow':
                css_content += "    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;\\n"
            elif frame_style == 'border':
                css_content += "    border: 2px solid var(--primary-color) !important;\\n"
            
            # Add position styles
            position = props.get('position', 'center')
            if position == 'left':
                css_content += "    margin-right: auto !important;\\n"
            elif position == 'right':
                css_content += "    margin-left: auto !important;\\n"
            elif position == 'center':
                css_content += "    margin: 0 auto !important;\\n"
            elif position == 'float-left':
                css_content += "    float: left !important; margin-right: 1rem !important;\\n"
            elif position == 'float-right':
                css_content += "    float: right !important; margin-left: 1rem !important;\\n"
            
            css_content += "}\\n\\n"
        
        # Add custom CSS from editor
        css_content += f"""
/* Custom CSS from editor */
{self.custom_css.get(1.0, tk.END)}
"""
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Add link to HTML if not present
        html_file = os.path.join(self.template_path, "index.html")
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'custom_editor_styles.css' not in content:
                # Add custom CSS link before closing head tag
                content = content.replace('</head>', 
                                        '    <link rel="stylesheet" href="custom_editor_styles.css">\\n</head>')
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    def export_website(self):
        """Export website with version control"""
        if not self.template_path:
            messagebox.showerror("Error", "No template loaded")
            return
        
        try:
            # Generate preview first
            self.generate_preview()
            
            # Create export directory
            version = self.version_var.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_name = f"{version}_{timestamp}"
            
            export_dir = os.path.join(os.path.dirname(self.template_path), export_name)
            
            # Copy template to export directory
            shutil.copytree(self.template_path, export_dir)
            
            # Save configuration
            config_file = os.path.join(export_dir, "website_config.json")
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.website_config, f, indent=2)
            
            # Create export info file
            info_file = os.path.join(export_dir, "EXPORT_INFO.txt")
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(f"""
Website Export Information
=========================

Export Version: {version}
Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Original Template: {self.template_path}

Configuration Summary:
- Title: {self.website_config["meta"]["title"]}
- Description: {self.website_config["meta"]["description"]}
- Brand: {self.website_config["navigation"]["title"]}
- Primary Color: {self.website_config["colors"]["primary"]}
- Logo: {self.website_config["logo"]["src"]}

Files Included:
- index.html (main website file)
- All original template files
- custom_editor_styles.css (your customizations)
- website_config.json (complete configuration backup)
- EXPORT_INFO.txt (this file)

To use this website:
1. Upload all files to your web server
2. Point your domain to index.html
3. Ensure all file permissions are correct

Generated by Website Template Editor v1.0
""")
            
            self.log_message(f"📦 Website exported to: {export_dir}")
            self.log_message(f"🏷️ Version: {version}")
            self.log_message(f"⏰ Timestamp: {timestamp}")
            
            # Update version for next export
            try:
                version_num = float(version.replace('v', ''))
                next_version = f"v{version_num + 0.1:.1f}"
                self.version_var.set(next_version)
            except:
                pass
            
            # Show success dialog with options
            result = messagebox.askyesno("Export Complete", 
                                       f"Website exported successfully to:\\n{export_dir}\\n\\nWould you like to open the export folder?")
            
            if result:
                # Open export folder in file manager
                import subprocess
                subprocess.call(["open", export_dir])  # macOS
            
        except Exception as e:
            self.log_message(f"❌ Export error: {e}")
            messagebox.showerror("Export Error", f"Could not export website: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.update_config_from_ui()
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.website_config, f, indent=2)
                self.log_message(f"💾 Configuration saved to: {file_path}")
                messagebox.showinfo("Success", "Configuration saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save configuration: {e}")
    
    def load_config(self):
        """Load configuration from file"""
        file_path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.website_config = json.load(f)
                
                self.update_ui_from_config()
                self.log_message(f"📁 Configuration loaded from: {file_path}")
                messagebox.showinfo("Success", "Configuration loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load configuration: {e}")
    
    def update_ui_from_config(self):
        """Update UI from loaded configuration"""
        # Meta information
        self.title_var.set(self.website_config["meta"]["title"])
        self.desc_var.set(self.website_config["meta"]["description"])
        
        # Navigation
        self.brand_var.set(self.website_config["navigation"]["title"])
        
        # Colors
        for key, var in self.color_vars.items():
            if key in self.website_config["colors"]:
                var.set(self.website_config["colors"][key])
                self.update_color_preview(key)
        
        # Logo
        self.logo_src_var.set(self.website_config["logo"]["src"])
        self.logo_width_var.set(self.website_config["logo"]["width"])
        self.logo_height_var.set(self.website_config["logo"]["height"])
    
    def log_message(self, message):
        """Add message to export log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\\n"
        self.export_log.insert(tk.END, log_entry)
        self.export_log.see(tk.END)
        self.root.update()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = WebsiteEditor()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
