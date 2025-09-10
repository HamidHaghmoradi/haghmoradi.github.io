#!/usr/bin/env python3
"""
Website Template Editor
A comprehensive Python interface for editing website templates with real-time preview.
Supports text editing, color customization, image management, responsive design, and more.
"""

import os
import json
import shutil
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox, scrolledtext
from PIL import Image, ImageTk
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
        
        # Tiles Manager Tab
        self.create_tiles_tab()
        
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
        ttk.Label(frame, text="Template Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        template_frame = ttk.LabelFrame(frame, text="Template Selection")
        template_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(template_frame, text="Load Template Folder", 
                  command=self.load_template_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.template_label = ttk.Label(template_frame, text="No template loaded")
        self.template_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Template info
        info_frame = ttk.LabelFrame(frame, text="Template Information")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.template_info = scrolledtext.ScrolledText(info_frame, height=20, width=80)
        self.template_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_content_tab(self):
        """Create content editing tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Content")
        
        # Meta information
        meta_frame = ttk.LabelFrame(frame, text="Website Meta Information")
        meta_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Title
        ttk.Label(meta_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.title_var = tk.StringVar(value=self.website_config["meta"]["title"])
        ttk.Entry(meta_frame, textvariable=self.title_var, width=60).grid(row=0, column=1, padx=5, pady=2)
        
        # Description
        ttk.Label(meta_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.desc_var = tk.StringVar(value=self.website_config["meta"]["description"])
        ttk.Entry(meta_frame, textvariable=self.desc_var, width=60).grid(row=1, column=1, padx=5, pady=2)
        
        # Navigation
        nav_frame = ttk.LabelFrame(frame, text="Navigation")
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(nav_frame, text="Brand Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.brand_var = tk.StringVar(value=self.website_config["navigation"]["title"])
        ttk.Entry(nav_frame, textvariable=self.brand_var, width=40).grid(row=0, column=1, padx=5, pady=2)
        
        # Content sections
        content_frame = ttk.LabelFrame(frame, text="Content Sections")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Section list
        self.section_listbox = tk.Listbox(content_frame, height=10)
        self.section_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Section controls
        section_controls = ttk.Frame(content_frame)
        section_controls.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(section_controls, text="Add Section", command=self.add_section).pack(fill=tk.X, pady=2)
        ttk.Button(section_controls, text="Edit Section", command=self.edit_section).pack(fill=tk.X, pady=2)
        ttk.Button(section_controls, text="Delete Section", command=self.delete_section).pack(fill=tk.X, pady=2)
        ttk.Button(section_controls, text="Move Up", command=self.move_section_up).pack(fill=tk.X, pady=2)
        ttk.Button(section_controls, text="Move Down", command=self.move_section_down).pack(fill=tk.X, pady=2)
    
    def create_design_tab(self):
        """Create design customization tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Design")
        
        # Color scheme
        color_frame = ttk.LabelFrame(frame, text="Color Scheme")
        color_frame.pack(fill=tk.X, padx=10, pady=5)
        
        colors = [
            ("Primary Color", "primary"),
            ("Secondary Color", "secondary"),
            ("Accent Color", "accent"),
            ("Background Color", "background"),
            ("Text Color", "text")
        ]
        
        self.color_vars = {}
        for i, (label, key) in enumerate(colors):
            ttk.Label(color_frame, text=label + ":").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            
            color_var = tk.StringVar(value=self.website_config["colors"][key])
            self.color_vars[key] = color_var
            
            color_entry = ttk.Entry(color_frame, textvariable=color_var, width=20)
            color_entry.grid(row=i, column=1, padx=5, pady=2)
            
            ttk.Button(color_frame, text="Choose", 
                      command=lambda k=key: self.choose_color(k)).grid(row=i, column=2, padx=5, pady=2)
        
        # Logo settings
        logo_frame = ttk.LabelFrame(frame, text="Logo Settings")
        logo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(logo_frame, text="Logo File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.logo_src_var = tk.StringVar(value=self.website_config["logo"]["src"])
        ttk.Entry(logo_frame, textvariable=self.logo_src_var, width=40).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(logo_frame, text="Browse", command=self.browse_logo).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(logo_frame, text="Width:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.logo_width_var = tk.StringVar(value=self.website_config["logo"]["width"])
        ttk.Entry(logo_frame, textvariable=self.logo_width_var, width=20).grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(logo_frame, text="Height:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.logo_height_var = tk.StringVar(value=self.website_config["logo"]["height"])
        ttk.Entry(logo_frame, textvariable=self.logo_height_var, width=20).grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        # CSS customization
        css_frame = ttk.LabelFrame(frame, text="Custom CSS")
        css_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.custom_css = scrolledtext.ScrolledText(css_frame, height=15, width=80)
        self.custom_css.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_image_tab(self):
        """Create image management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Images")
        
        # Image list
        list_frame = ttk.LabelFrame(frame, text="Image Gallery")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Image listbox with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.image_listbox = tk.Listbox(list_container)
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Image controls
        controls_frame = ttk.Frame(frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Add Image", command=self.add_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Remove Image", command=self.remove_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Edit Properties", command=self.edit_image_properties).pack(side=tk.LEFT, padx=5)
        
        # Image preview
        preview_frame = ttk.LabelFrame(frame, text="Image Preview")
        preview_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.image_preview_label = ttk.Label(preview_frame, text="Select an image to preview")
        self.image_preview_label.pack(pady=20)
        
        self.image_listbox.bind('<<ListboxSelect>>', self.on_image_select)
    
    def create_tiles_tab(self):
        """Create tiles management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tiles")
        
        # Tiles list
        tiles_frame = ttk.LabelFrame(frame, text="Tiles Gallery")
        tiles_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tiles_listbox = tk.Listbox(tiles_frame, height=15)
        self.tiles_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tile controls
        tile_controls = ttk.Frame(frame)
        tile_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(tile_controls, text="Add Tile", command=self.add_tile).pack(side=tk.LEFT, padx=5)
        ttk.Button(tile_controls, text="Edit Tile", command=self.edit_tile).pack(side=tk.LEFT, padx=5)
        ttk.Button(tile_controls, text="Delete Tile", command=self.delete_tile).pack(side=tk.LEFT, padx=5)
        ttk.Button(tile_controls, text="Duplicate Tile", command=self.duplicate_tile).pack(side=tk.LEFT, padx=5)
    
    def create_preview_tab(self):
        """Create preview and export tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Preview & Export")
        
        # Preview controls
        preview_controls = ttk.LabelFrame(frame, text="Preview Controls")
        preview_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(preview_controls, text="Start Preview Server", 
                  command=self.start_preview_server).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(preview_controls, text="Generate Preview", 
                  command=self.generate_preview).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(preview_controls, text="Open in Browser", 
                  command=self.open_preview).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Preview status
        self.preview_status = ttk.Label(preview_controls, text="Preview server stopped")
        self.preview_status.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Export controls
        export_frame = ttk.LabelFrame(frame, text="Export Website")
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(export_frame, text="Version Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.version_var = tk.StringVar(value="v1.1")
        ttk.Entry(export_frame, textvariable=self.version_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(export_frame, text="Export Website", 
                  command=self.export_website).grid(row=0, column=2, padx=5, pady=5)
        
        # Export log
        log_frame = ttk.LabelFrame(frame, text="Export Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.export_log = scrolledtext.ScrolledText(log_frame, height=20, width=80)
        self.export_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def load_template_dialog(self):
        """Load template from folder"""
        folder = filedialog.askdirectory(title="Select Template Folder")
        if folder:
            self.template_path = folder
            self.template_label.config(text=f"Template: {os.path.basename(folder)}")
            self.analyze_template()
    
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
        
        info = []
        info.append(f"Template Path: {self.template_path}")
        info.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info.append("")
        
        # Analyze files
        html_files = []
        css_files = []
        js_files = []
        image_files = []
        
        for root, dirs, files in os.walk(self.template_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.template_path)
                
                if file.endswith(('.html', '.htm')):
                    html_files.append(rel_path)
                elif file.endswith('.css'):
                    css_files.append(rel_path)
                elif file.endswith('.js'):
                    js_files.append(rel_path)
                elif file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')):
                    image_files.append(rel_path)
        
        info.append(f"HTML Files ({len(html_files)}):")
        for file in html_files:
            info.append(f"  - {file}")
        
        info.append(f"\\nCSS Files ({len(css_files)}):")
        for file in css_files:
            info.append(f"  - {file}")
        
        info.append(f"\\nJavaScript Files ({len(js_files)}):")
        for file in js_files:
            info.append(f"  - {file}")
        
        info.append(f"\\nImage Files ({len(image_files)}):")
        for file in image_files:
            info.append(f"  - {file}")
        
        self.template_info.delete(1.0, tk.END)
        self.template_info.insert(tk.END, "\\n".join(info))
        
        # Update image listbox
        self.update_image_list(image_files)
    
    def update_image_list(self, image_files):
        """Update image listbox"""
        self.image_listbox.delete(0, tk.END)
        for image_file in image_files:
            self.image_listbox.insert(tk.END, image_file)
    
    def choose_color(self, color_key):
        """Open color chooser"""
        color = colorchooser.askcolor(color=self.color_vars[color_key].get())[1]
        if color:
            self.color_vars[color_key].set(color)
    
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
            rel_path = os.path.relpath(file_path, self.template_path)
            if not rel_path.startswith('images/'):
                dest_path = os.path.join(self.template_path, 'images', os.path.basename(file_path))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(file_path, dest_path)
                rel_path = f"images/{os.path.basename(file_path)}"
            
            self.logo_src_var.set(rel_path)
    
    def add_section(self):
        """Add new content section"""
        self.section_dialog()
    
    def edit_section(self):
        """Edit selected section"""
        selection = self.section_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.website_config["sections"]):
                self.section_dialog(self.website_config["sections"][index], index)
    
    def delete_section(self):
        """Delete selected section"""
        selection = self.section_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.website_config["sections"]):
                self.website_config["sections"].pop(index)
                self.update_section_list()
    
    def move_section_up(self):
        """Move section up"""
        selection = self.section_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            sections = self.website_config["sections"]
            sections[index], sections[index-1] = sections[index-1], sections[index]
            self.update_section_list()
            self.section_listbox.selection_set(index-1)
    
    def move_section_down(self):
        """Move section down"""
        selection = self.section_listbox.curselection()
        if selection:
            index = selection[0]
            sections = self.website_config["sections"]
            if index < len(sections) - 1:
                sections[index], sections[index+1] = sections[index+1], sections[index]
                self.update_section_list()
                self.section_listbox.selection_set(index+1)
    
    def section_dialog(self, section_data=None, index=None):
        """Open section editor dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Section Editor")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        # Section data
        if section_data is None:
            section_data = {
                "type": "text",
                "title": "",
                "content": "",
                "image": "",
                "style": "default"
            }
        
        # Section type
        ttk.Label(dialog, text="Section Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        type_var = tk.StringVar(value=section_data.get("type", "text"))
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=["text", "image", "hero", "cards", "gallery"])
        type_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Section title
        ttk.Label(dialog, text="Title:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        title_var = tk.StringVar(value=section_data.get("title", ""))
        ttk.Entry(dialog, textvariable=title_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # Section content
        ttk.Label(dialog, text="Content:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        content_text = scrolledtext.ScrolledText(dialog, height=15, width=60)
        content_text.grid(row=2, column=1, padx=5, pady=5)
        content_text.insert(1.0, section_data.get("content", ""))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        def save_section():
            new_section = {
                "type": type_var.get(),
                "title": title_var.get(),
                "content": content_text.get(1.0, tk.END).strip(),
                "image": section_data.get("image", ""),
                "style": section_data.get("style", "default")
            }
            
            if index is not None:
                self.website_config["sections"][index] = new_section
            else:
                self.website_config["sections"].append(new_section)
            
            self.update_section_list()
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_section).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def update_section_list(self):
        """Update section listbox"""
        self.section_listbox.delete(0, tk.END)
        for i, section in enumerate(self.website_config["sections"]):
            title = section.get("title", f"Section {i+1}")
            section_type = section.get("type", "text")
            self.section_listbox.insert(tk.END, f"{i+1}. [{section_type}] {title}")
    
    def add_image(self):
        """Add new image"""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.svg;*.webp"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("PNG files", "*.png"),
                ("SVG files", "*.svg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path and self.template_path:
            # Copy to images directory
            images_dir = os.path.join(self.template_path, 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            dest_path = os.path.join(images_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)
            
            # Add to list
            rel_path = f"images/{os.path.basename(file_path)}"
            self.image_listbox.insert(tk.END, rel_path)
            
            self.log_message(f"Added image: {rel_path}")
    
    def remove_image(self):
        """Remove selected image"""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            image_path = self.image_listbox.get(index)
            
            # Confirm deletion
            if messagebox.askyesno("Confirm Delete", f"Delete {image_path}?"):
                full_path = os.path.join(self.template_path, image_path)
                try:
                    os.remove(full_path)
                    self.image_listbox.delete(index)
                    self.log_message(f"Removed image: {image_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file: {e}")
    
    def edit_image_properties(self):
        """Edit image properties"""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            image_path = self.image_listbox.get(index)
            self.image_properties_dialog(image_path)
    
    def image_properties_dialog(self, image_path):
        """Open image properties dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Image Properties - {os.path.basename(image_path)}")
        dialog.geometry("500x400")
        dialog.grab_set()
        
        # Current properties
        current_props = self.website_config["images"].get(image_path, {
            "alt": "",
            "width": "auto",
            "height": "auto",
            "frame": "none",
            "position": "center"
        })
        
        # Alt text
        ttk.Label(dialog, text="Alt Text:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        alt_var = tk.StringVar(value=current_props.get("alt", ""))
        ttk.Entry(dialog, textvariable=alt_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        
        # Dimensions
        ttk.Label(dialog, text="Width:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        width_var = tk.StringVar(value=current_props.get("width", "auto"))
        ttk.Entry(dialog, textvariable=width_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(dialog, text="Height:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        height_var = tk.StringVar(value=current_props.get("height", "auto"))
        ttk.Entry(dialog, textvariable=height_var, width=20).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Frame style
        ttk.Label(dialog, text="Frame:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        frame_var = tk.StringVar(value=current_props.get("frame", "none"))
        frame_combo = ttk.Combobox(dialog, textvariable=frame_var, 
                                  values=["none", "rounded", "circle", "shadow", "border"])
        frame_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Position
        ttk.Label(dialog, text="Position:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        position_var = tk.StringVar(value=current_props.get("position", "center"))
        position_combo = ttk.Combobox(dialog, textvariable=position_var, 
                                     values=["left", "center", "right", "float-left", "float-right"])
        position_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
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
        
        ttk.Button(button_frame, text="Save", command=save_properties).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def on_image_select(self, event):
        """Handle image selection"""
        selection = self.image_listbox.curselection()
        if selection:
            index = selection[0]
            image_path = self.image_listbox.get(index)
            self.show_image_preview(image_path)
    
    def show_image_preview(self, image_path):
        """Show image preview"""
        try:
            full_path = os.path.join(self.template_path, image_path)
            if os.path.exists(full_path) and not image_path.endswith('.svg'):
                # Load and resize image for preview
                image = Image.open(full_path)
                image.thumbnail((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.image_preview_label.config(image=photo, text="")
                self.image_preview_label.image = photo  # Keep reference
            else:
                self.image_preview_label.config(image="", text=f"Preview: {os.path.basename(image_path)}")
        except Exception as e:
            self.image_preview_label.config(image="", text=f"Error loading preview: {e}")
    
    def add_tile(self):
        """Add new tile"""
        self.tile_dialog()
    
    def edit_tile(self):
        """Edit selected tile"""
        selection = self.tiles_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.website_config["tiles"]):
                self.tile_dialog(self.website_config["tiles"][index], index)
    
    def delete_tile(self):
        """Delete selected tile"""
        selection = self.tiles_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.website_config["tiles"]):
                self.website_config["tiles"].pop(index)
                self.update_tiles_list()
    
    def duplicate_tile(self):
        """Duplicate selected tile"""
        selection = self.tiles_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.website_config["tiles"]):
                tile_data = self.website_config["tiles"][index].copy()
                tile_data["title"] += " (Copy)"
                self.website_config["tiles"].append(tile_data)
                self.update_tiles_list()
    
    def tile_dialog(self, tile_data=None, index=None):
        """Open tile editor dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tile Editor")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        if tile_data is None:
            tile_data = {
                "title": "",
                "description": "",
                "image": "",
                "link": "",
                "style": "default"
            }
        
        # Tile title
        ttk.Label(dialog, text="Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        title_var = tk.StringVar(value=tile_data.get("title", ""))
        ttk.Entry(dialog, textvariable=title_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        desc_text = scrolledtext.ScrolledText(dialog, height=8, width=60)
        desc_text.grid(row=1, column=1, padx=5, pady=5)
        desc_text.insert(1.0, tile_data.get("description", ""))
        
        # Image
        ttk.Label(dialog, text="Image:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        image_var = tk.StringVar(value=tile_data.get("image", ""))
        image_frame = ttk.Frame(dialog)
        image_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(image_frame, textvariable=image_var, width=40).pack(side=tk.LEFT)
        ttk.Button(image_frame, text="Browse", 
                  command=lambda: self.browse_tile_image(image_var)).pack(side=tk.LEFT, padx=5)
        
        # Link
        ttk.Label(dialog, text="Link:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        link_var = tk.StringVar(value=tile_data.get("link", ""))
        ttk.Entry(dialog, textvariable=link_var, width=50).grid(row=3, column=1, padx=5, pady=5)
        
        # Style
        ttk.Label(dialog, text="Style:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        style_var = tk.StringVar(value=tile_data.get("style", "default"))
        style_combo = ttk.Combobox(dialog, textvariable=style_var, 
                                  values=["default", "featured", "minimal", "card", "overlay"])
        style_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def save_tile():
            new_tile = {
                "title": title_var.get(),
                "description": desc_text.get(1.0, tk.END).strip(),
                "image": image_var.get(),
                "link": link_var.get(),
                "style": style_var.get()
            }
            
            if index is not None:
                self.website_config["tiles"][index] = new_tile
            else:
                self.website_config["tiles"].append(new_tile)
            
            self.update_tiles_list()
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_tile).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def browse_tile_image(self, image_var):
        """Browse for tile image"""
        file_path = filedialog.askopenfilename(
            title="Select Tile Image",
            filetypes=[
                ("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.svg;*.webp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path and self.template_path:
            # Copy to images directory
            images_dir = os.path.join(self.template_path, 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            dest_path = os.path.join(images_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)
            
            rel_path = f"images/{os.path.basename(file_path)}"
            image_var.set(rel_path)
    
    def update_tiles_list(self):
        """Update tiles listbox"""
        self.tiles_listbox.delete(0, tk.END)
        for i, tile in enumerate(self.website_config["tiles"]):
            title = tile.get("title", f"Tile {i+1}")
            self.tiles_listbox.insert(tk.END, f"{i+1}. {title}")
    
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
                    self.log_message(f"Preview server started at http://localhost:{self.preview_port}")
                    self.preview_status.config(text=f"Server running on port {self.preview_port}")
                    httpd.serve_forever()
            except Exception as e:
                self.log_message(f"Server error: {e}")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
    
    def stop_preview_server(self):
        """Stop preview server"""
        # Note: This is a simplified stop - in production you'd want proper server shutdown
        self.preview_status.config(text="Preview server stopped")
        self.log_message("Preview server stopped")
    
    def open_preview(self):
        """Open preview in browser"""
        webbrowser.open(f"http://localhost:{self.preview_port}")
    
    def generate_preview(self):
        """Generate preview files"""
        if not self.template_path:
            messagebox.showerror("Error", "No template loaded")
            return
        
        try:
            self.update_config_from_ui()
            self.apply_config_to_files()
            self.log_message("Preview generated successfully")
        except Exception as e:
            self.log_message(f"Error generating preview: {e}")
            messagebox.showerror("Error", f"Could not generate preview: {e}")
    
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
            
            # Update logo
            content = re.sub(r'<img src="[^"]*" alt="[^"]*" class="logo-icon">', 
                           f'<img src="{self.website_config["logo"]["src"]}" alt="{self.website_config["logo"]["alt"]}" class="logo-icon">', content)
            
            # Update brand name
            content = re.sub(r'<span class="logo-text">.*?</span>', 
                           f'<span class="logo-text">{self.website_config["navigation"]["title"]}</span>', content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Update CSS file with custom styles
        self.update_css_file()
    
    def update_css_file(self):
        """Update CSS file with custom styles"""
        css_file = os.path.join(self.template_path, "custom_styles.css")
        
        css_content = f"""
/* Generated Custom Styles */
:root {{
    --primary-color: {self.website_config["colors"]["primary"]};
    --secondary-color: {self.website_config["colors"]["secondary"]};
    --accent-color: {self.website_config["colors"]["accent"]};
    --background-color: {self.website_config["colors"]["background"]};
    --text-color: {self.website_config["colors"]["text"]};
}}

.logo-icon {{
    width: {self.website_config["logo"]["width"]} !important;
    height: {self.website_config["logo"]["height"]} !important;
}}

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
            
            if 'custom_styles.css' not in content:
                # Add custom CSS link before closing head tag
                content = content.replace('</head>', 
                                        '    <link rel="stylesheet" href="custom_styles.css">\\n</head>')
                
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
            
            self.log_message(f"Website exported to: {export_dir}")
            self.log_message(f"Version: {version}")
            self.log_message(f"Timestamp: {timestamp}")
            
            messagebox.showinfo("Export Complete", f"Website exported to:\\n{export_dir}")
            
        except Exception as e:
            self.log_message(f"Export error: {e}")
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
                self.log_message(f"Configuration saved to: {file_path}")
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
                self.log_message(f"Configuration loaded from: {file_path}")
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
            var.set(self.website_config["colors"][key])
        
        # Logo
        self.logo_src_var.set(self.website_config["logo"]["src"])
        self.logo_width_var.set(self.website_config["logo"]["width"])
        self.logo_height_var.set(self.website_config["logo"]["height"])
        
        # Update lists
        self.update_section_list()
        self.update_tiles_list()
    
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
    app = WebsiteEditor()
    app.run()

if __name__ == "__main__":
    main()
