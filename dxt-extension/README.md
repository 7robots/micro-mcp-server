# Micro.blog Books Desktop Extension (DXT)

A Desktop Extension (DXT) version of the Micro.blog Books MCP server that provides seamless integration with Claude Desktop for managing your Micro.blog book collections, bookshelves, and reading goals.

## Features

### 📚 Bookshelf Management
- **get_bookshelves**: Get all your bookshelves
- **get_bookshelf_books**: Get books in a specific bookshelf
- **add_bookshelf**: Create a new bookshelf
- **rename_bookshelf**: Rename an existing bookshelf

### 📖 Book Management
- **add_book**: Add a new book to a bookshelf
- **move_book**: Move a book between bookshelves
- **remove_book**: Remove a book from a bookshelf
- **change_book_cover**: Update a book's cover image

### 🎯 Reading Goals
- **get_reading_goals**: Get your reading goals
- **get_goal_progress**: Get progress toward a specific reading goal
- **update_reading_goal**: Update a reading goal's target or progress

## Installation

### Prerequisites

- **Claude Desktop** (version 0.7.0 or higher)
- **Node.js** (version 18.0.0 or higher)
- **Micro.blog account** with API access

### Quick Installation

1. **Download the extension package** (`.dxt` file)
2. **Open Claude Desktop**
3. **Install the extension**:
   - Go to Settings → Extensions
   - Click "Install Extension"
   - Select the downloaded `.dxt` file
4. **Configure your bearer token**:
   - Enter your Micro.blog bearer token when prompted
   - You can get this from your Micro.blog account settings

### Manual Installation (Development)

If you want to install from source:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/7robots/micro-mcp-server.git
   cd micro-mcp-server/dxt-extension
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Package the extension**:
   ```bash
   # Using the dxt CLI tool (if available)
   dxt pack .
   
   # Or manually create a zip file with all contents
   zip -r micro-blog-books.dxt . -x "node_modules/*" ".git/*"
   ```

4. **Install in Claude Desktop** as described above

## Configuration

### Bearer Token Setup

You'll need a bearer token from Micro.blog to authenticate API requests:

1. **Log into your Micro.blog account**
2. **Go to Account Settings**
3. **Generate or copy your API bearer token**
4. **Enter this token during extension installation**

The token is stored securely in your local configuration and is only used to make API requests to Micro.blog on your behalf.

## Usage

Once installed, you can ask Claude to help manage your books. Here are some example commands:

### Getting Information
- "Show me all my bookshelves"
- "What books are in my 'Currently Reading' bookshelf?"
- "What are my reading goals for this year?"
- "How much progress have I made on goal 123?"

### Managing Bookshelves
- "Create a new bookshelf called 'Science Fiction'"
- "Rename bookshelf 5 to 'Favorites'"

### Managing Books
- "Add 'Project Hail Mary' by Andy Weir to my 'Currently Reading' bookshelf"
- "Move book 79 to bookshelf 23"
- "Remove book 45 from bookshelf 12"
- "Change the cover of book 67 in bookshelf 8 to this URL: https://example.com/cover.jpg"

### Managing Reading Goals
- "Update my reading goal 1 to target 25 books"
- "Set my progress on goal 2 to 15 books read"

## Security & Privacy

- **Local Operation**: This extension runs entirely on your local machine
- **Secure Token Storage**: Your bearer token is stored securely in Claude Desktop's configuration
- **API-Only Access**: The extension only makes API calls to Micro.blog's official endpoints
- **No Data Collection**: No usage data is collected or transmitted to third parties
- **Open Source**: The code is open source and auditable

## Troubleshooting

### Common Issues

1. **"Bearer token is required" error**:
   - Make sure you've entered your Micro.blog bearer token during installation
   - Verify the token is valid by checking your Micro.blog account settings

2. **"Network error" messages**:
   - Check your internet connection
   - Verify that micro.blog is accessible from your network
   - Check if you're behind a corporate firewall that might block the requests

3. **"HTTP 401" or authentication errors**:
   - Your bearer token may have expired or been revoked
   - Generate a new token in your Micro.blog account settings
   - Reinstall the extension with the new token

4. **Extension not appearing in Claude Desktop**:
   - Ensure you're using Claude Desktop version 0.7.0 or higher
   - Verify Node.js 18.0.0+ is installed on your system
   - Check that the extension package was installed correctly

### Debug Mode

To run the extension in debug mode for troubleshooting:

```bash
cd dxt-extension
export MICRO_BLOG_BEARER_TOKEN="your_token_here"
npm run dev
```

This will start the server with inspection enabled, allowing you to debug any issues.

### Getting Help

- **GitHub Issues**: Report bugs or request features at [GitHub Issues](https://github.com/7robots/micro-mcp-server/issues)
- **Documentation**: Check the main project [README](../README.md) for additional information
- **Micro.blog API**: For API-specific issues, refer to the [Micro.blog Books API documentation](https://help.micro.blog/t/books-api/280)

## Development

### Project Structure

```
dxt-extension/
├── manifest.json          # Extension metadata and configuration
├── package.json          # Node.js project configuration
├── server/
│   └── index.js          # MCP server implementation
└── README.md             # This file
```

### Building from Source

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Test the server**:
   ```bash
   export MICRO_BLOG_BEARER_TOKEN="your_token_here"
   npm start
   ```

3. **Package the extension**:
   ```bash
   # Create a zip file with all necessary files
   zip -r micro-blog-books.dxt . -x "node_modules/*" ".git/*" "*.log"
   ```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Related Projects

- **Main MCP Server**: The original Python-based MCP server in the parent directory
- **Modal Deployment**: Modal.com deployment version in the `modal/` directory
- **Desktop Extensions**: Official DXT specifications at [anthropics/dxt](https://github.com/anthropics/dxt)