#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const BASE_URL = "https://micro.blog";

/**
 * HTTP client for Micro.blog Books API
 */
class MicroBooksClient {
  constructor(bearerToken) {
    if (!bearerToken) {
      throw new Error("Bearer token is required");
    }
    this.bearerToken = bearerToken;
    this.headers = {
      "Authorization": `Bearer ${bearerToken}`,
      "User-Agent": "Micro Books MCP Server DXT/1.0.0",
      "Content-Type": "application/x-www-form-urlencoded",
    };
  }

  async makeRequest(path, options = {}) {
    const url = new URL(path, BASE_URL);
    const requestOptions = {
      ...options,
      headers: {
        ...this.headers,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, requestOptions);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${response.statusText}${errorText ? ` - ${errorText}` : ''}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error(`Network error: Unable to connect to ${url}`);
      }
      throw error;
    }
  }

  async getBookshelves() {
    return await this.makeRequest("/books/bookshelves");
  }

  async getBookshelfBooks(bookshelfId) {
    if (!Number.isInteger(bookshelfId) || bookshelfId <= 0) {
      throw new Error("Bookshelf ID must be a positive integer");
    }
    return await this.makeRequest(`/books/bookshelves/${bookshelfId}`);
  }

  async addBookshelf(name) {
    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      throw new Error("Bookshelf name is required and must be a non-empty string");
    }
    
    await this.makeRequest("/books/bookshelves", {
      method: "POST",
      body: new URLSearchParams({ name: name.trim() }),
    });
    
    return { success: true, message: `Bookshelf '${name.trim()}' created successfully` };
  }

  async renameBookshelf(bookshelfId, name) {
    if (!Number.isInteger(bookshelfId) || bookshelfId <= 0) {
      throw new Error("Bookshelf ID must be a positive integer");
    }
    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      throw new Error("Bookshelf name is required and must be a non-empty string");
    }

    await this.makeRequest(`/books/bookshelves/${bookshelfId}`, {
      method: "POST",
      body: new URLSearchParams({ name: name.trim() }),
    });

    return { success: true, message: `Bookshelf renamed to '${name.trim()}' successfully` };
  }

  async addBook(title, author, bookshelfId, isbn = null, coverUrl = null) {
    if (!title || typeof title !== 'string' || title.trim().length === 0) {
      throw new Error("Book title is required and must be a non-empty string");
    }
    if (!author || typeof author !== 'string' || author.trim().length === 0) {
      throw new Error("Book author is required and must be a non-empty string");
    }
    if (!Number.isInteger(bookshelfId) || bookshelfId <= 0) {
      throw new Error("Bookshelf ID must be a positive integer");
    }

    const data = {
      title: title.trim(),
      author: author.trim(),
      bookshelf_id: bookshelfId.toString(),
    };

    if (isbn && typeof isbn === 'string' && isbn.trim().length > 0) {
      data.isbn = isbn.trim();
    }
    if (coverUrl && typeof coverUrl === 'string' && coverUrl.trim().length > 0) {
      data.cover_url = coverUrl.trim();
    }

    await this.makeRequest("/books", {
      method: "POST",
      body: new URLSearchParams(data),
    });

    return { success: true, message: `Book '${title.trim()}' by ${author.trim()} added successfully` };
  }

  async moveBook(bookId, bookshelfId) {
    if (!Number.isInteger(bookId) || bookId <= 0) {
      throw new Error("Book ID must be a positive integer");
    }
    if (!Number.isInteger(bookshelfId) || bookshelfId <= 0) {
      throw new Error("Bookshelf ID must be a positive integer");
    }

    await this.makeRequest(`/books/bookshelves/${bookshelfId}/assign`, {
      method: "POST",
      body: new URLSearchParams({ book_id: bookId.toString() }),
    });

    return { success: true, message: `Book moved to bookshelf ${bookshelfId} successfully` };
  }

  async removeBook(bookshelfId, bookId) {
    if (!Number.isInteger(bookshelfId) || bookshelfId <= 0) {
      throw new Error("Bookshelf ID must be a positive integer");
    }
    if (!Number.isInteger(bookId) || bookId <= 0) {
      throw new Error("Book ID must be a positive integer");
    }

    await this.makeRequest(`/books/bookshelves/${bookshelfId}/remove/${bookId}`, {
      method: "DELETE",
    });

    return { success: true, message: "Book removed from bookshelf successfully" };
  }

  async changeBookCover(bookshelfId, bookId, coverUrl) {
    if (!Number.isInteger(bookshelfId) || bookshelfId <= 0) {
      throw new Error("Bookshelf ID must be a positive integer");
    }
    if (!Number.isInteger(bookId) || bookId <= 0) {
      throw new Error("Book ID must be a positive integer");
    }
    if (!coverUrl || typeof coverUrl !== 'string' || coverUrl.trim().length === 0) {
      throw new Error("Cover URL is required and must be a non-empty string");
    }

    await this.makeRequest(`/books/bookshelves/${bookshelfId}/cover/${bookId}`, {
      method: "POST",
      body: new URLSearchParams({ cover_url: coverUrl.trim() }),
    });

    return { success: true, message: "Book cover updated successfully" };
  }

  async getReadingGoals() {
    return await this.makeRequest("/books/goals");
  }

  async getGoalProgress(goalId) {
    if (!Number.isInteger(goalId) || goalId <= 0) {
      throw new Error("Goal ID must be a positive integer");
    }
    return await this.makeRequest(`/books/goals/${goalId}`);
  }

  async updateReadingGoal(goalId, value, progress = null) {
    if (!Number.isInteger(goalId) || goalId <= 0) {
      throw new Error("Goal ID must be a positive integer");
    }
    if (!Number.isInteger(value) || value <= 0) {
      throw new Error("Goal value must be a positive integer");
    }

    const data = { value: value.toString() };
    if (progress !== null) {
      if (!Number.isInteger(progress) || progress < 0) {
        throw new Error("Progress must be a non-negative integer");
      }
      data.progress = progress.toString();
    }

    await this.makeRequest(`/books/goals/${goalId}`, {
      method: "POST",
      body: new URLSearchParams(data),
    });

    return { success: true, message: "Reading goal updated successfully" };
  }
}

/**
 * Create and configure the MCP server
 */
function createServer() {
  const server = new Server(
    {
      name: "micro-blog-books",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // Get bearer token from environment
  const bearerToken = process.env.MICRO_BLOG_BEARER_TOKEN;
  if (!bearerToken) {
    console.error("Error: MICRO_BLOG_BEARER_TOKEN environment variable is required");
    process.exit(1);
  }

  // Create client instance
  let client;
  try {
    client = new MicroBooksClient(bearerToken);
  } catch (error) {
    console.error("Error: Failed to initialize Micro.blog client:", error.message);
    process.exit(1);
  }

  // Define available tools
  const tools = [
    {
      name: "get_bookshelves",
      description: "Get all bookshelves from Micro.blog",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
    {
      name: "get_bookshelf_books",
      description: "Get books in a specific bookshelf",
      inputSchema: {
        type: "object",
        properties: {
          bookshelf_id: {
            type: "integer",
            description: "The ID of the bookshelf to get books from",
            minimum: 1,
          },
        },
        required: ["bookshelf_id"],
      },
    },
    {
      name: "add_bookshelf",
      description: "Create a new bookshelf",
      inputSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "The name of the new bookshelf",
            minLength: 1,
          },
        },
        required: ["name"],
      },
    },
    {
      name: "rename_bookshelf",
      description: "Rename an existing bookshelf",
      inputSchema: {
        type: "object",
        properties: {
          bookshelf_id: {
            type: "integer",
            description: "The ID of the bookshelf to rename",
            minimum: 1,
          },
          name: {
            type: "string",
            description: "The new name for the bookshelf",
            minLength: 1,
          },
        },
        required: ["bookshelf_id", "name"],
      },
    },
    {
      name: "add_book",
      description: "Add a new book to a bookshelf",
      inputSchema: {
        type: "object",
        properties: {
          title: {
            type: "string",
            description: "The title of the book",
            minLength: 1,
          },
          author: {
            type: "string",
            description: "The author of the book",
            minLength: 1,
          },
          bookshelf_id: {
            type: "integer",
            description: "The ID of the bookshelf to add the book to",
            minimum: 1,
          },
          isbn: {
            type: "string",
            description: "The ISBN of the book (optional)",
          },
          cover_url: {
            type: "string",
            description: "URL to the book cover image (optional)",
          },
        },
        required: ["title", "author", "bookshelf_id"],
      },
    },
    {
      name: "move_book",
      description: "Move a book to a different bookshelf",
      inputSchema: {
        type: "object",
        properties: {
          book_id: {
            type: "integer",
            description: "The ID of the book to move",
            minimum: 1,
          },
          bookshelf_id: {
            type: "integer",
            description: "The ID of the target bookshelf",
            minimum: 1,
          },
        },
        required: ["book_id", "bookshelf_id"],
      },
    },
    {
      name: "remove_book",
      description: "Remove a book from a bookshelf",
      inputSchema: {
        type: "object",
        properties: {
          bookshelf_id: {
            type: "integer",
            description: "The ID of the bookshelf",
            minimum: 1,
          },
          book_id: {
            type: "integer",
            description: "The ID of the book to remove",
            minimum: 1,
          },
        },
        required: ["bookshelf_id", "book_id"],
      },
    },
    {
      name: "change_book_cover",
      description: "Change the cover image for a book",
      inputSchema: {
        type: "object",
        properties: {
          bookshelf_id: {
            type: "integer",
            description: "The ID of the bookshelf",
            minimum: 1,
          },
          book_id: {
            type: "integer",
            description: "The ID of the book",
            minimum: 1,
          },
          cover_url: {
            type: "string",
            description: "URL to the new cover image",
            minLength: 1,
          },
        },
        required: ["bookshelf_id", "book_id", "cover_url"],
      },
    },
    {
      name: "get_reading_goals",
      description: "Get all reading goals",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
    {
      name: "get_goal_progress",
      description: "Get progress toward a specific reading goal",
      inputSchema: {
        type: "object",
        properties: {
          goal_id: {
            type: "integer",
            description: "The ID of the reading goal",
            minimum: 1,
          },
        },
        required: ["goal_id"],
      },
    },
    {
      name: "update_reading_goal",
      description: "Update a reading goal's target or progress",
      inputSchema: {
        type: "object",
        properties: {
          goal_id: {
            type: "integer",
            description: "The ID of the reading goal",
            minimum: 1,
          },
          value: {
            type: "integer",
            description: "The target number of books for the goal",
            minimum: 1,
          },
          progress: {
            type: "integer",
            description: "The current progress (number of books read, optional)",
            minimum: 0,
          },
        },
        required: ["goal_id", "value"],
      },
    },
  ];

  // Handle list tools requests
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: tools,
    };
  });

  // Handle tool call requests
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      switch (name) {
        case "get_bookshelves": {
          const result = await client.getBookshelves();
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "get_bookshelf_books": {
          const { bookshelf_id } = args;
          const result = await client.getBookshelfBooks(bookshelf_id);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "add_bookshelf": {
          const { name } = args;
          const result = await client.addBookshelf(name);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "rename_bookshelf": {
          const { bookshelf_id, name } = args;
          const result = await client.renameBookshelf(bookshelf_id, name);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "add_book": {
          const { title, author, bookshelf_id, isbn, cover_url } = args;
          const result = await client.addBook(title, author, bookshelf_id, isbn, cover_url);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "move_book": {
          const { book_id, bookshelf_id } = args;
          const result = await client.moveBook(book_id, bookshelf_id);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "remove_book": {
          const { bookshelf_id, book_id } = args;
          const result = await client.removeBook(bookshelf_id, book_id);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "change_book_cover": {
          const { bookshelf_id, book_id, cover_url } = args;
          const result = await client.changeBookCover(bookshelf_id, book_id, cover_url);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "get_reading_goals": {
          const result = await client.getReadingGoals();
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "get_goal_progress": {
          const { goal_id } = args;
          const result = await client.getGoalProgress(goal_id);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        case "update_reading_goal": {
          const { goal_id, value, progress } = args;
          const result = await client.updateReadingGoal(goal_id, value, progress);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        }

        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    } catch (error) {
      const errorMessage = `Error executing ${name}: ${error.message}`;
      console.error(errorMessage);
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: true,
              message: errorMessage,
              tool: name,
              timestamp: new Date().toISOString(),
            }, null, 2),
          },
        ],
        isError: true,
      };
    }
  });

  return server;
}

/**
 * Main function to start the server
 */
async function main() {
  console.error("Starting Micro.blog Books MCP Server...");
  
  try {
    const server = createServer();
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    console.error("✓ Micro.blog Books MCP Server running");
  } catch (error) {
    console.error("✗ Failed to start server:", error.message);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.error('Received SIGINT, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.error('Received SIGTERM, shutting down gracefully...');
  process.exit(0);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
  process.exit(1);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Start the server
main().catch((error) => {
  console.error("Failed to start server:", error);
  process.exit(1);
});