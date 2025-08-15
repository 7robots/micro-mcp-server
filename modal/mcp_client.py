#!/usr/bin/env python3
"""
MCP Client to connect to the Modal-deployed MCP server and make tool calls.
"""

import asyncio
import json
from typing import Dict, Any
import httpx
from fastmcp import Client


class MCPClient:
    """Client for connecting to MCP server over HTTP."""
    
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.session_id = None
    
    async def initialize(self) -> Dict[str, Any]:
        """Initialize the MCP session."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.server_url}/initialize",
                json={
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "mcp-client",
                        "version": "1.0.0"
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            self.session_id = response.headers.get('x-session-id')
            return result
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools from the server."""
        async with httpx.AsyncClient() as client:
            headers = {}
            if self.session_id:
                headers['x-session-id'] = self.session_id
                
            response = await client.post(
                f"{self.server_url}/tools/list",
                json={},
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a specific tool with given arguments."""
        if arguments is None:
            arguments = {}
            
        async with httpx.AsyncClient() as client:
            headers = {}
            if self.session_id:
                headers['x-session-id'] = self.session_id
                
            response = await client.post(
                f"{self.server_url}/tools/call",
                json={
                    "name": tool_name,
                    "arguments": arguments
                },
                headers=headers
            )
            response.raise_for_status()
            return response.json()


async def main():
    # Replace with your actual Modal deployment URL
    # Format: https://your-app-name--modal-domain.modal.run
    server_url = input("Enter your Modal server URL: ").strip()
    
    if not server_url:
        print("Error: Please provide a valid server URL")
        return
    
    # Ensure URL ends with /mcp/ for FastMCP
    if not server_url.endswith('/mcp/'):
        if server_url.endswith('/'):
            server_url += 'mcp/'
        else:
            server_url += '/mcp/'
    
    def extract_content(result):
        """Extract text content from MCP response."""
        if isinstance(result, list) and len(result) > 0:
            content = result[0].text if hasattr(result[0], 'text') else str(result[0])
            try:
                data = json.loads(content)
                return json.dumps(data, indent=2)
            except json.JSONDecodeError:
                return content
        return str(result)

    try:
        async with Client(server_url) as client:
            print("✓ Connected to FastMCP server")
            
            # Ping to verify connection
            await client.ping()
            print("✓ Ping successful\n")
            
            while True:
                print("Available tools:")
                print("1. get_bookshelves - Get all bookshelves")
                print("2. get_bookshelf_books - Get books from a specific bookshelf")  
                print("3. add_bookshelf - Create a new bookshelf")
                print("4. rename_bookshelf - Rename an existing bookshelf")
                print("5. add_book - Add a new book to a bookshelf")
                print("6. move_book - Move a book to a different bookshelf")
                print("7. remove_book - Remove a book from a bookshelf")
                print("8. change_book_cover - Change a book's cover image")
                print("9. get_reading_goals - Get all reading goals")
                print("10. get_goal_progress - Get progress toward a specific goal")
                print("11. update_reading_goal - Update a reading goal")
                print("12. quit - Exit the client")
                
                choice = input("\nSelect a tool (1-12): ").strip()
                
                if choice == "12" or choice.lower() == "quit":
                    print("Goodbye!")
                    break
                elif choice == "1":
                    print("\nCalling get_bookshelves...")
                    result = await client.call_tool("get_bookshelves")
                    print("✓ Tool call successful!")
                    print(f"Result:\n{extract_content(result)}")
                    
                elif choice == "2":
                    bookshelf_id = input("Enter bookshelf ID: ").strip()
                    try:
                        bookshelf_id = int(bookshelf_id)
                        print(f"\nCalling get_bookshelf_books with ID {bookshelf_id}...")
                        result = await client.call_tool("get_bookshelf_books", {"bookshelf_id": bookshelf_id})
                        print("✓ Tool call successful!")
                        print(f"Result:\n{extract_content(result)}")
                    except ValueError:
                        print("✗ Error: Please enter a valid integer for bookshelf ID")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "3":
                    name = input("Enter new bookshelf name: ").strip()
                    if name:
                        print(f"\nCalling add_bookshelf with name '{name}'...")
                        try:
                            result = await client.call_tool("add_bookshelf", {"name": name})
                            print("✓ Tool call successful!")
                            print(f"Result:\n{extract_content(result)}")
                        except Exception as e:
                            print(f"✗ Error: {str(e)}")
                    else:
                        print("✗ Error: Bookshelf name cannot be empty")
                        
                elif choice == "4":
                    bookshelf_id = input("Enter bookshelf ID to rename: ").strip()
                    name = input("Enter new name: ").strip()
                    try:
                        bookshelf_id = int(bookshelf_id)
                        if name:
                            print(f"\nCalling rename_bookshelf with ID {bookshelf_id} and name '{name}'...")
                            result = await client.call_tool("rename_bookshelf", {"bookshelf_id": bookshelf_id, "name": name})
                            print("✓ Tool call successful!")
                            print(f"Result:\n{extract_content(result)}")
                        else:
                            print("✗ Error: Bookshelf name cannot be empty")
                    except ValueError:
                        print("✗ Error: Please enter a valid integer for bookshelf ID")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "5":
                    title = input("Enter book title: ").strip()
                    author = input("Enter book author: ").strip()
                    bookshelf_id = input("Enter bookshelf ID: ").strip()
                    isbn = input("Enter ISBN (optional, press Enter to skip): ").strip()
                    cover_url = input("Enter cover URL (optional, press Enter to skip): ").strip()
                    
                    try:
                        bookshelf_id = int(bookshelf_id)
                        if title and author:
                            args = {"title": title, "author": author, "bookshelf_id": bookshelf_id}
                            if isbn:
                                args["isbn"] = isbn
                            if cover_url:
                                args["cover_url"] = cover_url
                                
                            print(f"\nCalling add_book with title '{title}' by {author}...")
                            result = await client.call_tool("add_book", args)
                            print("✓ Tool call successful!")
                            print(f"Result:\n{extract_content(result)}")
                        else:
                            print("✗ Error: Title and author are required")
                    except ValueError:
                        print("✗ Error: Please enter a valid integer for bookshelf ID")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "6":
                    book_id = input("Enter book ID to move: ").strip()
                    bookshelf_id = input("Enter target bookshelf ID: ").strip()
                    try:
                        book_id = int(book_id)
                        bookshelf_id = int(bookshelf_id)
                        print(f"\nCalling move_book with book ID {book_id} to bookshelf {bookshelf_id}...")
                        result = await client.call_tool("move_book", {"book_id": book_id, "bookshelf_id": bookshelf_id})
                        print("✓ Tool call successful!")
                        print(f"Result:\n{extract_content(result)}")
                    except ValueError:
                        print("✗ Error: Please enter valid integers for book ID and bookshelf ID")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "7":
                    bookshelf_id = input("Enter bookshelf ID: ").strip()
                    book_id = input("Enter book ID to remove: ").strip()
                    try:
                        bookshelf_id = int(bookshelf_id)
                        book_id = int(book_id)
                        print(f"\nCalling remove_book with book ID {book_id} from bookshelf {bookshelf_id}...")
                        result = await client.call_tool("remove_book", {"bookshelf_id": bookshelf_id, "book_id": book_id})
                        print("✓ Tool call successful!")
                        print(f"Result:\n{extract_content(result)}")
                    except ValueError:
                        print("✗ Error: Please enter valid integers for bookshelf ID and book ID")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "8":
                    bookshelf_id = input("Enter bookshelf ID: ").strip()
                    book_id = input("Enter book ID: ").strip()
                    cover_url = input("Enter new cover URL: ").strip()
                    try:
                        bookshelf_id = int(bookshelf_id)
                        book_id = int(book_id)
                        if cover_url:
                            print(f"\nCalling change_book_cover for book {book_id} in bookshelf {bookshelf_id}...")
                            result = await client.call_tool("change_book_cover", {"bookshelf_id": bookshelf_id, "book_id": book_id, "cover_url": cover_url})
                            print("✓ Tool call successful!")
                            print(f"Result:\n{extract_content(result)}")
                        else:
                            print("✗ Error: Cover URL is required")
                    except ValueError:
                        print("✗ Error: Please enter valid integers for bookshelf ID and book ID")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "9":
                    print("\nCalling get_reading_goals...")
                    try:
                        result = await client.call_tool("get_reading_goals")
                        print("✓ Tool call successful!")
                        print(f"Result:\n{extract_content(result)}")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "10":
                    goal_id = input("Enter goal ID: ").strip()
                    try:
                        goal_id = int(goal_id)
                        print(f"\nCalling get_goal_progress with goal ID {goal_id}...")
                        result = await client.call_tool("get_goal_progress", {"goal_id": goal_id})
                        print("✓ Tool call successful!")
                        print(f"Result:\n{extract_content(result)}")
                    except ValueError:
                        print("✗ Error: Please enter a valid integer for goal ID")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                elif choice == "11":
                    goal_id = input("Enter goal ID: ").strip()
                    value = input("Enter target value (number of books): ").strip()
                    progress = input("Enter current progress (optional, press Enter to skip): ").strip()
                    
                    try:
                        goal_id = int(goal_id)
                        value = int(value)
                        args = {"goal_id": goal_id, "value": value}
                        
                        if progress:
                            try:
                                progress = int(progress)
                                args["progress"] = progress
                            except ValueError:
                                print("✗ Error: Progress must be a valid integer")
                                continue
                                
                        print(f"\nCalling update_reading_goal for goal {goal_id} with target {value}...")
                        result = await client.call_tool("update_reading_goal", args)
                        print("✓ Tool call successful!")
                        print(f"Result:\n{extract_content(result)}")
                    except ValueError:
                        print("✗ Error: Please enter valid integers for goal ID and target value")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                        
                else:
                    print("✗ Invalid choice. Please select 1-12.")
                
                print("\n" + "="*50 + "\n")
                
    except Exception as e:
        print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    print("MCP Client for Modal-deployed MCP Server")
    print("=" * 40)
    asyncio.run(main())