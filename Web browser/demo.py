#!/usr/bin/env python3
"""
Demo script for the Python Web Browser
This script demonstrates various browser features and capabilities
"""

import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import os

def show_demo_info():
    """Show information about the browser demo"""
    demo_text = """
    Python Web Browser Demo
    ======================
    
    This demo showcases the features of the Python Web Browser:
    
    🚀 Core Features:
    • Tabbed browsing with unlimited tabs
    • Smart address bar with search integration
    • Navigation controls (back, forward, reload, home)
    • Bookmark management system
    • Complete browsing history
    • Downloads tracking
    
    🎨 User Interface:
    • Modern, intuitive design
    • Responsive layout
    • Full keyboard shortcuts
    • Status bar with progress indicator
    • Comprehensive menu system
    
    🔧 Advanced Features:
    • Settings and preferences
    • File operations (open/save)
    • Text search functionality
    • Zoom controls
    • Error handling and user feedback
    
    🎯 Try These Features:
    1. Open multiple tabs (Ctrl+T)
    2. Navigate to websites (try google.com)
    3. Use the search bar for queries
    4. Add bookmarks (Ctrl+D)
    5. View browsing history
    6. Try keyboard shortcuts
    7. Open local HTML files
    8. Explore the menu system
    
    Ready to start browsing? Click 'Launch Browser' below!
    """
    
    root = tk.Tk()
    root.title("Python Web Browser Demo")
    root.geometry("600x500")
    root.resizable(False, False)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Create main frame
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="Python Web Browser Demo", 
                          font=("Arial", 16, "bold"), fg="blue")
    title_label.pack(pady=(0, 20))
    
    # Demo text
    text_widget = tk.Text(main_frame, wrap=tk.WORD, height=20, width=70,
                         font=("Arial", 10), bg="#f0f0f0", fg="black")
    text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    text_widget.insert(1.0, demo_text)
    text_widget.config(state=tk.DISABLED)
    
    # Buttons frame
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.X)
    
    def launch_browser():
        """Launch the web browser"""
        try:
            # Import and run the browser
            from web_browser import main as browser_main
            root.destroy()  # Close demo window
            browser_main()  # Launch browser
        except ImportError as e:
            messagebox.showerror("Error", f"Could not import browser: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch browser: {e}")
    
    def open_github():
        """Open GitHub repository"""
        webbrowser.open("https://github.com")
    
    def open_documentation():
        """Open documentation"""
        if os.path.exists("README.md"):
            webbrowser.open("file://" + os.path.abspath("README.md"))
        else:
            messagebox.showinfo("Documentation", "README.md not found in current directory")
    
    def show_shortcuts():
        """Show keyboard shortcuts"""
        shortcuts_text = """
        Keyboard Shortcuts:
        ===================
        
        Navigation:
        • Ctrl+T - New Tab
        • Ctrl+N - New Window
        • Ctrl+W - Close Tab
        • Ctrl+Tab - Next Tab
        • Ctrl+Shift+Tab - Previous Tab
        
        File Operations:
        • Ctrl+O - Open File
        • Ctrl+S - Save Page
        • Ctrl+Q - Quit Browser
        
        Browsing:
        • F5 - Reload Page
        • Esc - Stop Loading
        • Ctrl+D - Add Bookmark
        • Ctrl+F - Find Text
        
        Zoom:
        • Ctrl++ - Zoom In
        • Ctrl+- - Zoom Out
        • Ctrl+0 - Reset Zoom
        """
        
        shortcuts_window = tk.Toplevel(root)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("400x500")
        shortcuts_window.transient(root)
        shortcuts_window.grab_set()
        
        text_widget = tk.Text(shortcuts_window, wrap=tk.WORD, font=("Arial", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, shortcuts_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(shortcuts_window, text="Close", 
                  command=shortcuts_window.destroy).pack(pady=10)
    
    # Buttons
    tk.Button(button_frame, text="🚀 Launch Browser", command=launch_browser,
             font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
             padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="📖 Documentation", command=open_documentation,
             font=("Arial", 10), bg="#2196F3", fg="white",
             padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="⌨️ Shortcuts", command=show_shortcuts,
             font=("Arial", 10), bg="#FF9800", fg="white",
             padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="🌐 GitHub", command=open_github,
             font=("Arial", 10), bg="#9C27B0", fg="white",
             padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="❌ Exit", command=root.quit,
             font=("Arial", 10), bg="#F44336", fg="white",
             padx=15, pady=8).pack(side=tk.RIGHT, padx=5)
    
    # Start the demo
    root.mainloop()

if __name__ == "__main__":
    show_demo_info()
