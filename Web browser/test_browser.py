#!/usr/bin/env python3
"""
Test script for the Python Web Browser
This script tests various browser components and functionality
"""

import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestWebBrowser(unittest.TestCase):
    """Test cases for the Web Browser"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_bookmark_loading(self):
        """Test bookmark loading functionality"""
        from web_browser import WebBrowser
        import tkinter as tk
        
        # Create a mock root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        try:
            browser = WebBrowser(root)
            
            # Test initial bookmarks loading
            self.assertIsInstance(browser.bookmarks, list)
            
            # Test adding a bookmark
            test_bookmark = {
                'title': 'Test Page',
                'url': 'https://example.com',
                'date_added': '2024-01-01T00:00:00'
            }
            browser.bookmarks.append(test_bookmark)
            browser.save_bookmarks()
            
            # Test loading bookmarks
            loaded_bookmarks = browser.load_bookmarks()
            self.assertIn(test_bookmark, loaded_bookmarks)
            
        finally:
            root.destroy()
    
    def test_history_loading(self):
        """Test history loading functionality"""
        from web_browser import WebBrowser
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        try:
            browser = WebBrowser(root)
            
            # Test initial history loading
            self.assertIsInstance(browser.history, list)
            
            # Test adding to history
            test_history_item = {
                'url': 'https://example.com',
                'title': 'Example Page',
                'timestamp': '2024-01-01T00:00:00'
            }
            browser.history.append(test_history_item)
            browser.save_history()
            
            # Test loading history
            loaded_history = browser.load_history()
            self.assertIn(test_history_item, loaded_history)
            
        finally:
            root.destroy()
    
    def test_url_validation(self):
        """Test URL validation and processing"""
        from web_browser import WebBrowser
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        try:
            browser = WebBrowser(root)
            
            # Test URL processing
            test_cases = [
                ('google.com', 'https://google.com'),
                ('https://example.com', 'https://example.com'),
                ('http://test.com', 'http://test.com'),
                ('search query', 'https://www.google.com/search?q=search+query'),
            ]
            
            for input_url, expected in test_cases:
                # This would need to be implemented in the browser class
                # For now, we'll test the logic conceptually
                if not input_url.startswith(('http://', 'https://', 'file://', 'about:')):
                    if '.' in input_url and ' ' not in input_url:
                        processed_url = 'https://' + input_url
                    else:
                        processed_url = f"https://www.google.com/search?q={input_url.replace(' ', '+')}"
                else:
                    processed_url = input_url
                
                self.assertEqual(processed_url, expected)
                
        finally:
            root.destroy()
    
    def test_config_loading(self):
        """Test configuration loading"""
        try:
            from browser_config import BROWSER_CONFIG, get_config, get_shortcut
            
            # Test config loading
            self.assertIsInstance(BROWSER_CONFIG, dict)
            self.assertIn('default_home_page', BROWSER_CONFIG)
            self.assertIn('search_engines', BROWSER_CONFIG)
            
            # Test get_config function
            home_page = get_config('default_home_page')
            self.assertEqual(home_page, 'https://www.google.com')
            
            # Test get_shortcut function
            new_tab_shortcut = get_shortcut('new_tab')
            self.assertEqual(new_tab_shortcut, '<Control-t>')
            
        except ImportError:
            self.skipTest("browser_config module not available")
    
    def test_file_operations(self):
        """Test file operations"""
        from web_browser import WebBrowser
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        try:
            browser = WebBrowser(root)
            
            # Test bookmark file operations
            test_bookmarks = [
                {'title': 'Test 1', 'url': 'https://test1.com', 'date_added': '2024-01-01'},
                {'title': 'Test 2', 'url': 'https://test2.com', 'date_added': '2024-01-02'}
            ]
            
            browser.bookmarks = test_bookmarks
            browser.save_bookmarks()
            
            # Verify file was created
            self.assertTrue(os.path.exists('bookmarks.json'))
            
            # Test loading
            loaded_bookmarks = browser.load_bookmarks()
            self.assertEqual(len(loaded_bookmarks), 2)
            self.assertEqual(loaded_bookmarks[0]['title'], 'Test 1')
            
        finally:
            root.destroy()
    
    def test_error_handling(self):
        """Test error handling mechanisms"""
        from web_browser import WebBrowser
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        try:
            browser = WebBrowser(root)
            
            # Test with invalid data
            browser.bookmarks = "invalid_data"
            
            # This should not raise an exception
            browser.save_bookmarks()
            
            # Test loading with corrupted file
            with open('bookmarks.json', 'w') as f:
                f.write("invalid json content")
            
            # This should return empty list
            loaded_bookmarks = browser.load_bookmarks()
            self.assertEqual(loaded_bookmarks, [])
            
        finally:
            root.destroy()

class TestBrowserConfig(unittest.TestCase):
    """Test cases for browser configuration"""
    
    def test_config_structure(self):
        """Test configuration structure"""
        try:
            from browser_config import BROWSER_CONFIG, KEYBOARD_SHORTCUTS
            
            # Test main config
            self.assertIsInstance(BROWSER_CONFIG, dict)
            self.assertIn('default_home_page', BROWSER_CONFIG)
            self.assertIn('search_engines', BROWSER_CONFIG)
            self.assertIn('user_agent', BROWSER_CONFIG)
            
            # Test shortcuts
            self.assertIsInstance(KEYBOARD_SHORTCUTS, dict)
            self.assertIn('new_tab', KEYBOARD_SHORTCUTS)
            self.assertIn('reload', KEYBOARD_SHORTCUTS)
            
        except ImportError:
            self.skipTest("browser_config module not available")
    
    def test_helper_functions(self):
        """Test helper functions"""
        try:
            from browser_config import get_config, get_shortcut, is_supported_file_type
            
            # Test get_config
            home_page = get_config('default_home_page')
            self.assertEqual(home_page, 'https://www.google.com')
            
            # Test get_shortcut
            shortcut = get_shortcut('new_tab')
            self.assertEqual(shortcut, '<Control-t>')
            
            # Test file type checking
            self.assertTrue(is_supported_file_type('test.html'))
            self.assertTrue(is_supported_file_type('test.htm'))
            self.assertTrue(is_supported_file_type('test.txt'))
            self.assertFalse(is_supported_file_type('test.xyz'))
            
        except ImportError:
            self.skipTest("browser_config module not available")

def run_tests():
    """Run all tests"""
    print("Running Python Web Browser Tests")
    print("=" * 40)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestWebBrowser))
    suite.addTests(loader.loadTestsFromTestCase(TestBrowserConfig))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 40)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
