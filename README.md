# Micro.blog Books MCP Server

An MCP (Model Context Protocol) server built with FastMCP that provides access to the Micro.blog Books API, allowing Claude Desktop (or other MCP clients) to manage your book collections, bookshelves, and reading goals.

## Overview

This server enables Claude Desktop to interact directly with your Micro.blog book collection through a clean set of tools that cover all aspects of book management - from organizing bookshelves to tracking reading goals. Built with FastMCP for simplicity and reliability.

## Features

This MCP server provides the following tools for managing your Micro.blog books:

### Bookshelf Management
- **get_bookshelves**: Get all your bookshelves
- **get_bookshelf_books**: Get books in a specific bookshelf
- **add_bookshelf**: Create a new bookshelf
- **rename_bookshelf**: Rename an existing bookshelf

### Book Management
- **add_book**: Add a new book to a bookshelf
- **move_book**: Move a book between bookshelves
- **remove_book**: Remove a book from a bookshelf
- **change_book_cover**: Update a book's cover image

### Reading Goals
- **get_reading_goals**: Get your reading goals
- **get_goal_progress**: Get progress toward a specific reading goal
- **update_reading_goal**: Update a reading goal's target or progress

## Prerequisites

- **Python 3.8 or higher** (FastMCP has lower requirements)
- **Micro.blog account** with API access
- **Claude Desktop** application

## Installation

### Quick Setup (Recommended)

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/micro-mcp-server.git
   cd micro-mcp-server
   ```

2. **Run the automated setup:**
   ```bash
   python install.py
   ```
   This installs FastMCP and all dependencies, then verifies everything works.

### Manual Setup

If you prefer manual installation:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This installs FastMCP and all required packages.

2. **Verify installation:**
   ```bash
   python run_server.py --help
   ```

## Setup

### 1. Get Your Micro.blog Bearer Token

You'll need a bearer token from Micro.blog to authenticate API requests. You can get this from your Micro.blog account settings.

### 2. Configure Environment

Set your bearer token as an environment variable:

```bash
export MICRO_BLOG_BEARER_TOKEN="your_token_here"
```

### 3. Configure Claude Desktop

#### Option A: Automatic Configuration (Recommended)

Run the configuration generator:

```bash
python get_config.py
```

This will output the exact configuration you need and save it to `claude_desktop_config.json`.

#### Option B: Manual Configuration

Add the MCP server to your Claude Desktop configuration. The configuration file is typically located at:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following to your configuration:

```json
{
  "mcpServers": {
    "micro-books": {
      "command": "/opt/anaconda3/bin/python3",
      "args": [
        "/path/to/micro-mcp-server/run_server.py"
      ],
      "env": {
        "MICRO_BLOG_BEARER_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Important Notes:**
- The configuration generator automatically finds a compatible Python version
- Replace `your_token_here` with your actual Micro.blog bearer token
- Use **full absolute paths** for both the Python executable and script

### 4. Restart Claude Desktop

After updating the configuration, restart Claude Desktop for the changes to take effect.

## Usage

Once configured, you can ask Claude to help manage your books. For example:

- "Show me all my bookshelves"
- "Add a new book called 'Project Hail Mary' by Andy Weir to my 'Currently reading' bookshelf"
- "Move book ID 79 to bookshelf ID 23"
- "What are my reading goals for this year?"
- "Update my reading goal to 25 books"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## API Reference

All tools return JSON responses from the Micro.blog API. The server handles authentication automatically using your bearer token.

For more details about the underlying API, see the [Micro.blog Books API documentation](https://help.micro.blog/t/books-api/280).

## Troubleshooting

1. **Authentication errors**: Make sure your `MICRO_BLOG_BEARER_TOKEN` is set correctly and valid
2. **Server not appearing in Claude**: Check that the path in your configuration is correct and that uv is installed
3. **Permission errors**: Ensure the server files have appropriate permissions

## Development

To run the server in development mode:

```bash
cd micro-mcp-server
python run_server.py --bearer-token "your_token_here"
```

## Troubleshooting

### Common Issues

1. **`spawn python ENOENT` error**: This means Claude Desktop can't find the Python executable. Use the configuration generator (`python get_config.py`) to get the correct paths.

2. **Import errors**: Make sure you've run the setup script (`python install.py`) to install FastMCP and dependencies.

3. **Authentication errors**: Verify your `MICRO_BLOG_BEARER_TOKEN` is set correctly and valid in the Claude Desktop configuration.

4. **Path errors**: Ensure both the Python executable and `run_server.py` paths are **full absolute paths** in your configuration.

### Testing the Server

You can test the server independently:

```bash
# Test with your actual token
python run_server.py --bearer-token "your_actual_token"

# Or test the installation
python install.py
```
