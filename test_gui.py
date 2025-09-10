#!/usr/bin/env python3
"""
Simple Website Editor Test
Testing basic functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os

def test_gui():
    """Test basic GUI functionality"""
    try:
        root = tk.Tk()
        root.title("Website Editor - Test")
        root.geometry("600x400")
        
        # Test basic widgets
        ttk.Label(root, text="Website Editor Test", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(root, text="If you can see this, the GUI is working!").pack(pady=10)
        
        def test_click():
            messagebox.showinfo("Success", "GUI is working properly!")
        
        ttk.Button(root, text="Test Button", command=test_click).pack(pady=10)
        
        # Check current directory
        current_dir = os.getcwd()
        ttk.Label(root, text=f"Current directory: {current_dir}").pack(pady=5)
        
        # Check for index.html
        index_exists = os.path.exists("index.html")
        ttk.Label(root, text=f"index.html exists: {index_exists}").pack(pady=5)
        
        def close_app():
            root.destroy()
        
        ttk.Button(root, text="Close", command=close_app).pack(pady=20)
        
        print("Starting GUI test...")
        root.mainloop()
        print("GUI test completed")
        
    except Exception as e:
        print(f"Error in GUI test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing GUI components...")
    test_gui()
