# Desktop Extension (DXT) Installation Guide

This guide will help you install the Micro.blog Books MCP Server as a Desktop Extension (DXT) in Claude Desktop.

## What is a Desktop Extension (DXT)?

Desktop Extensions are a new way to install MCP servers as single-click extensions, similar to browser extensions. They provide:

- ✅ **Easy installation** - Just install a `.dxt` file
- ✅ **Automatic dependency management** - No need to install Node.js packages manually
- ✅ **Secure configuration** - Tokens stored securely in Claude Desktop
- ✅ **One-click setup** - No command line required

## Prerequisites

- **Claude Desktop** version 0.7.0 or higher
- **Micro.blog account** with API access
- **Internet connection** for API calls

## Installation Steps

### 1. Get Your Micro.blog Bearer Token

1. Log into your [Micro.blog account](https://micro.blog)
2. Go to **Account Settings**
3. Find or generate your **API bearer token**
4. Copy this token (you'll need it in step 3)

### 2. Download the Extension

You have two options:

#### Option A: Download Pre-built Extension
- Download `micro-blog-books.dxt` from the [releases page](https://github.com/7robots/micro-mcp-server/releases)

#### Option B: Build from Source
```bash
git clone https://github.com/7robots/micro-mcp-server.git
cd micro-mcp-server/dxt-extension
npm install
npm run build
```
This creates `micro-blog-books.dxt` in the `dxt-extension` directory.

### 3. Install in Claude Desktop

1. **Open Claude Desktop**
2. **Go to Settings** (gear icon)
3. **Navigate to Extensions**
4. **Click "Install Extension"**
5. **Select the `.dxt` file** you downloaded/built
6. **Enter your bearer token** when prompted
7. **Restart Claude Desktop**

### 4. Verify Installation

Ask Claude something like:
- "Show me my bookshelves"
- "What are my reading goals?"

If the extension is working, Claude will be able to access your Micro.blog books data!

## Troubleshooting

### Extension Not Appearing
- Ensure you're using Claude Desktop 0.7.0+
- Check that the `.dxt` file installed without errors
- Try restarting Claude Desktop

### Authentication Errors
- Verify your bearer token is correct
- Check that it has the necessary permissions in Micro.blog
- Try regenerating the token and reinstalling the extension

### Network Errors
- Check your internet connection
- Verify that micro.blog is accessible from your network
- Check firewall settings if you're on a corporate network

## Features Available

Once installed, you can ask Claude to:

### 📚 Manage Bookshelves
- "Show me all my bookshelves"
- "Create a new bookshelf called 'Science Fiction'"
- "Rename my 'To Read' bookshelf to 'Reading Queue'"

### 📖 Manage Books
- "Add 'Dune' by Frank Herbert to my 'Science Fiction' bookshelf"
- "Move book ID 123 to my 'Favorites' bookshelf"
- "Remove the book with ID 456 from my 'Currently Reading' shelf"

### 🎯 Track Reading Goals
- "What are my reading goals for this year?"
- "Update my reading goal to target 30 books"
- "How much progress have I made on my reading goal?"

## Security & Privacy

- **Local Processing**: The extension runs entirely on your machine
- **Secure Storage**: Your bearer token is encrypted and stored securely by Claude Desktop
- **No Data Collection**: No usage analytics or personal data is collected
- **API-Only Access**: Only makes requests to official Micro.blog API endpoints

## Getting Help

- **Issues**: Report problems on [GitHub Issues](https://github.com/7robots/micro-mcp-server/issues)
- **Documentation**: See the [main README](README.md) for additional information
- **Micro.blog API**: Check [Micro.blog's API docs](https://help.micro.blog/t/books-api/280) for API-specific questions

## Uninstalling

To remove the extension:

1. Open Claude Desktop Settings
2. Go to Extensions
3. Find "Micro.blog Books" in the list
4. Click "Remove" or "Uninstall"
5. Restart Claude Desktop

Your bearer token and all extension data will be removed from your system.

---

**Enjoy managing your book collection with Claude! 📚**