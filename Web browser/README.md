# Python Web Browser

A modern, feature-rich web browser built entirely with Python and Tkinter. This browser provides a complete browsing experience with advanced features typically found in commercial browsers.

## Features

### Core Browsing
- **Tabbed Browsing**: Open multiple websites in separate tabs
- **Navigation Controls**: Back, forward, reload, and home buttons
- **Address Bar**: Smart URL input with auto-completion
- **Search Integration**: Automatic search for non-URL inputs
- **HTML Rendering**: Clean text-based rendering of web pages

### Advanced Features
- **Bookmarks System**: Save, organize, and manage your favorite websites
- **Browsing History**: Track and revisit previously visited pages
- **Downloads Manager**: Monitor and manage downloaded files
- **Settings Panel**: Customize browser behavior and preferences
- **Keyboard Shortcuts**: Full keyboard navigation support
- **Zoom Controls**: Adjust text size for better readability

### User Interface
- **Modern Design**: Clean, intuitive interface
- **Status Bar**: Real-time loading status and progress
- **Menu System**: Comprehensive menu with all browser functions
- **Responsive Layout**: Adapts to different window sizes

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Browser
```bash
python web_browser.py
```

## Usage

### Basic Navigation
- **Address Bar**: Type a URL or search term and press Enter
- **Navigation Buttons**: Use ← → ↻ 🏠 buttons for navigation
- **Tabs**: Click the "+" button or use Ctrl+T to open new tabs
- **Bookmarks**: Click ★ to bookmark the current page

### Keyboard Shortcuts
- `Ctrl+T`: New tab
- `Ctrl+N`: New window
- `Ctrl+O`: Open file
- `Ctrl+S`: Save page
- `Ctrl+D`: Add bookmark
- `Ctrl+F`: Find text
- `F5`: Reload page
- `Esc`: Stop loading
- `Ctrl++`: Zoom in
- `Ctrl+-`: Zoom out
- `Ctrl+0`: Reset zoom

### Menu Functions

#### File Menu
- **New Tab/Window**: Open new browsing contexts
- **Open File**: Load local HTML files
- **Save Page As**: Save current page to disk
- **Exit**: Close the browser

#### Edit Menu
- **Cut/Copy/Paste**: Standard text operations
- **Find**: Search for text on current page

#### View Menu
- **Reload**: Refresh current page
- **Stop**: Cancel page loading
- **Zoom Controls**: Adjust text size

#### Bookmarks Menu
- **Add Bookmark**: Save current page
- **Bookmark Manager**: Organize saved bookmarks
- **Quick Access**: Recently bookmarked pages

#### History Menu
- **Show History**: View browsing history
- **Clear History**: Remove all history records

#### Tools Menu
- **Downloads**: View download history
- **Settings**: Configure browser preferences

## Technical Details

### Architecture
The browser is built using a modular architecture with the following components:

- **WebBrowser Class**: Main application controller
- **Tab Management**: Individual tab handling and state management
- **HTTP Client**: Web request handling using the `requests` library
- **HTML Parser**: Content extraction using `BeautifulSoup`
- **Data Persistence**: JSON-based storage for bookmarks and history

### Dependencies
- **tkinter**: GUI framework (included with Python)
- **requests**: HTTP client library
- **beautifulsoup4**: HTML parsing
- **Pillow**: Image processing (for future enhancements)

### File Structure
```
web_browser/
├── web_browser.py      # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── bookmarks.json     # Saved bookmarks (created on first use)
├── history.json       # Browsing history (created on first use)
└── browser_settings.json # User settings (created on first use)
```

## Customization

### Settings
Access the settings panel through Tools → Settings to configure:
- Home page URL
- Default search engine
- Browser preferences

### Bookmarks
- Add bookmarks using Ctrl+D or the bookmark button
- Organize bookmarks through the Bookmark Manager
- Quick access through the Bookmarks menu

### History
- View complete browsing history
- Clear history for privacy
- Quick navigation to previously visited pages

## Advanced Features

### Tab Management
- **Multiple Tabs**: Open unlimited tabs
- **Tab Switching**: Click tabs or use keyboard shortcuts
- **Tab History**: Each tab maintains its own navigation history
- **Tab Titles**: Dynamic tab titles based on page content

### Search Integration
- **Smart URL Detection**: Automatically detects URLs vs search queries
- **Search Engine Integration**: Configurable search providers
- **Search Suggestions**: Enhanced search experience

### Data Management
- **Persistent Storage**: Bookmarks and history saved between sessions
- **Data Export**: Save bookmarks and history to files
- **Privacy Controls**: Clear history and data on demand

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Connection Issues**: Check internet connection and firewall settings

3. **Page Loading Errors**: Some websites may block automated requests

4. **Memory Usage**: Close unused tabs to improve performance

### Performance Tips
- Close unused tabs regularly
- Clear browsing history periodically
- Use the stop button if pages load slowly
- Restart the browser if it becomes unresponsive

## Future Enhancements

### Planned Features
- **JavaScript Support**: Basic JavaScript execution
- **CSS Rendering**: Improved visual rendering
- **Image Support**: Display images in web pages
- **Extension System**: Plugin architecture
- **Sync Features**: Cloud synchronization
- **Privacy Mode**: Incognito browsing
- **Developer Tools**: Web development utilities

### Contributing
This is an educational project designed to demonstrate web browser concepts. Feel free to:
- Report bugs and issues
- Suggest new features
- Submit code improvements
- Create documentation

## License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## Educational Value

This browser implementation demonstrates:
- **GUI Programming**: Tkinter interface design
- **Network Programming**: HTTP requests and responses
- **Data Parsing**: HTML content extraction
- **State Management**: Tab and session handling
- **File I/O**: Data persistence
- **Threading**: Asynchronous operations
- **Event Handling**: User interaction management

Perfect for learning web browser internals and Python GUI development!

---

**Note**: This browser is designed for educational purposes and basic web browsing. For production use, consider using established browsers like Chrome, Firefox, or Safari.
