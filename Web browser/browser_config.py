#!/usr/bin/env python3
"""
Configuration file for the Python Web Browser
Contains default settings and customizable options
"""

# Browser Configuration
BROWSER_CONFIG = {
    # Default settings
    'default_home_page': 'https://www.google.com',
    'default_search_engine': 'Google',
    'search_engines': {
        'Google': 'https://www.google.com/search?q={}',
        'Bing': 'https://www.bing.com/search?q={}',
        'DuckDuckGo': 'https://duckduckgo.com/?q={}',
        'Yahoo': 'https://search.yahoo.com/search?p={}'
    },
    
    # Window settings
    'default_window_size': (1200, 800),
    'minimum_window_size': (800, 600),
    'window_title': 'Python Web Browser',
    
    # Tab settings
    'max_tab_title_length': 20,
    'default_new_tab_url': 'about:blank',
    
    # Request settings
    'request_timeout': 10,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    
    # History settings
    'max_history_items': 1000,
    'max_bookmarks': 500,
    
    # UI settings
    'default_font': ('Arial', 10),
    'min_font_size': 8,
    'max_font_size': 24,
    'font_size_step': 2,
    
    # File settings
    'bookmarks_file': 'bookmarks.json',
    'history_file': 'history.json',
    'settings_file': 'browser_settings.json',
    'downloads_folder': 'downloads',
    
    # Feature flags
    'enable_javascript': False,  # Future feature
    'enable_images': False,     # Future feature
    'enable_css': False,        # Future feature
    'enable_cookies': True,
    'enable_cache': True,
    
    # Privacy settings
    'clear_history_on_exit': False,
    'private_browsing': False,
    'track_analytics': False,
}

# Keyboard shortcuts configuration
KEYBOARD_SHORTCUTS = {
    'new_tab': '<Control-t>',
    'new_window': '<Control-n>',
    'open_file': '<Control-o>',
    'save_page': '<Control-s>',
    'quit': '<Control-q>',
    'add_bookmark': '<Control-d>',
    'reload': '<F5>',
    'stop_loading': '<Escape>',
    'zoom_in': '<Control-plus>',
    'zoom_out': '<Control-minus>',
    'reset_zoom': '<Control-0>',
    'find_text': '<Control-f>',
    'close_tab': '<Control-w>',
    'next_tab': '<Control-Tab>',
    'previous_tab': '<Control-Shift-Tab>',
}

# Supported file types
SUPPORTED_FILE_TYPES = {
    'html': ['.html', '.htm'],
    'text': ['.txt', '.text'],
    'json': ['.json'],
    'xml': ['.xml'],
    'css': ['.css'],
    'js': ['.js', '.javascript'],
}

# HTTP status codes and their meanings
HTTP_STATUS_CODES = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',
    301: 'Moved Permanently',
    302: 'Found',
    304: 'Not Modified',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    408: 'Request Timeout',
    410: 'Gone',
    429: 'Too Many Requests',
    500: 'Internal Server Error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}

# Common MIME types
MIME_TYPES = {
    'text/html': 'HTML Document',
    'text/plain': 'Text Document',
    'text/css': 'CSS Stylesheet',
    'text/javascript': 'JavaScript File',
    'application/json': 'JSON Document',
    'application/xml': 'XML Document',
    'image/jpeg': 'JPEG Image',
    'image/png': 'PNG Image',
    'image/gif': 'GIF Image',
    'image/svg+xml': 'SVG Image',
    'application/pdf': 'PDF Document',
    'application/zip': 'ZIP Archive',
}

# Browser themes (for future implementation)
THEMES = {
    'light': {
        'bg_color': '#ffffff',
        'fg_color': '#000000',
        'select_bg': '#0078d4',
        'select_fg': '#ffffff',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
    },
    'dark': {
        'bg_color': '#2d2d2d',
        'fg_color': '#ffffff',
        'select_bg': '#0078d4',
        'select_fg': '#ffffff',
        'entry_bg': '#404040',
        'entry_fg': '#ffffff',
    },
    'high_contrast': {
        'bg_color': '#000000',
        'fg_color': '#ffffff',
        'select_bg': '#ffff00',
        'select_fg': '#000000',
        'entry_bg': '#000000',
        'entry_fg': '#ffffff',
    }
}

# Error messages
ERROR_MESSAGES = {
    'connection_error': 'Unable to connect to the server. Please check your internet connection.',
    'timeout_error': 'The request timed out. The server may be slow or unavailable.',
    'not_found': 'The requested page was not found (404 Error).',
    'forbidden': 'Access to this page is forbidden (403 Error).',
    'server_error': 'The server encountered an error (500 Error).',
    'invalid_url': 'The URL is invalid or malformed.',
    'file_not_found': 'The specified file could not be found.',
    'permission_denied': 'Permission denied to access the file.',
    'unknown_error': 'An unknown error occurred.',
}

# Success messages
SUCCESS_MESSAGES = {
    'bookmark_added': 'Page added to bookmarks successfully.',
    'bookmark_removed': 'Bookmark removed successfully.',
    'history_cleared': 'Browsing history cleared successfully.',
    'settings_saved': 'Settings saved successfully.',
    'page_saved': 'Page saved successfully.',
    'download_completed': 'Download completed successfully.',
}

# Default bookmarks
DEFAULT_BOOKMARKS = [
    {
        'title': 'Google',
        'url': 'https://www.google.com',
        'date_added': '2024-01-01T00:00:00'
    },
    {
        'title': 'Python.org',
        'url': 'https://www.python.org',
        'date_added': '2024-01-01T00:00:00'
    },
    {
        'title': 'GitHub',
        'url': 'https://github.com',
        'date_added': '2024-01-01T00:00:00'
    },
    {
        'title': 'Stack Overflow',
        'url': 'https://stackoverflow.com',
        'date_added': '2024-01-01T00:00:00'
    }
]

# About page content
ABOUT_CONTENT = """
Python Web Browser v1.0.0
========================

Welcome to the Python Web Browser!

This is a fully functional web browser built entirely with Python and Tkinter.
It demonstrates modern web browser concepts and provides a complete browsing experience.

Features:
• Tabbed browsing with unlimited tabs
• Bookmarks management system
• Complete browsing history tracking
• Downloads manager
• Search engine integration
• Modern, intuitive user interface
• Full keyboard shortcut support
• Customizable settings and preferences

Technical Details:
• Built with Python 3.7+
• GUI framework: Tkinter
• HTTP client: Requests library
• HTML parsing: BeautifulSoup4
• Data storage: JSON files

This browser is perfect for:
• Learning web browser internals
• Understanding HTTP protocols
• GUI programming with Tkinter
• Python application development
• Educational purposes

Version: 1.0.0
Build Date: 2024
License: MIT
Author: Python Web Browser Team

© 2024 Python Web Browser. All rights reserved.
"""

def get_config(key, default=None):
    """Get configuration value by key"""
    return BROWSER_CONFIG.get(key, default)

def get_shortcut(action):
    """Get keyboard shortcut for an action"""
    return KEYBOARD_SHORTCUTS.get(action, '')

def get_error_message(error_type):
    """Get user-friendly error message"""
    return ERROR_MESSAGES.get(error_type, ERROR_MESSAGES['unknown_error'])

def get_success_message(message_type):
    """Get user-friendly success message"""
    return SUCCESS_MESSAGES.get(message_type, '')

def is_supported_file_type(filename):
    """Check if file type is supported"""
    ext = '.' + filename.split('.')[-1].lower()
    for file_type, extensions in SUPPORTED_FILE_TYPES.items():
        if ext in extensions:
            return True
    return False

def get_file_type_description(filename):
    """Get description for file type"""
    ext = '.' + filename.split('.')[-1].lower()
    for mime_type, description in MIME_TYPES.items():
        if ext in ['.html', '.htm'] and 'html' in mime_type:
            return description
        elif ext in ['.txt'] and 'plain' in mime_type:
            return description
        elif ext in ['.css'] and 'css' in mime_type:
            return description
        elif ext in ['.js'] and 'javascript' in mime_type:
            return description
    return 'Unknown File Type'
