#!/usr/bin/env python3
"""Micro.blog Books API MCP Server using FastMCP - Desktop Extension Version."""

import json
import logging
import os
import sys
from typing import Optional
from urllib.parse import urljoin

# Check Python version compatibility early
if sys.version_info < (3, 10):
    print(f"Error: This extension requires Python 3.10 or higher.", file=sys.stderr)
    print(f"Current version: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Please upgrade your Python installation:", file=sys.stderr)
    print("- macOS: Install from python.org or use Homebrew: brew install python", file=sys.stderr)
    print("- Windows: Download from python.org", file=sys.stderr) 
    print("- Linux: Use your package manager (e.g., sudo apt install python3.10)", file=sys.stderr)
    sys.exit(1)

import httpx
from fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://micro.blog"


class MicroBooksClient:
    """HTTP client for Micro.blog Books API."""

    def __init__(self, bearer_token: str) -> None:
        self.bearer_token = bearer_token
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "Micro Books MCP Server DXT/1.0.0",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    async def get_bookshelves(self) -> dict:
        """Get all bookshelves."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                urljoin(BASE_URL, "/books/bookshelves"),
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_bookshelf_books(self, bookshelf_id: int) -> dict:
        """Get books in a specific bookshelf."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                urljoin(BASE_URL, f"/books/bookshelves/{bookshelf_id}"),
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def add_bookshelf(self, name: str) -> dict:
        """Add a new bookshelf."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(BASE_URL, "/books/bookshelves"),
                headers=self.headers,
                data={"name": name},
            )
            response.raise_for_status()
            return {"success": True, "message": f"Bookshelf '{name}' created successfully"}

    async def rename_bookshelf(self, bookshelf_id: int, name: str) -> dict:
        """Rename a bookshelf."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(BASE_URL, f"/books/bookshelves/{bookshelf_id}"),
                headers=self.headers,
                data={"name": name},
            )
            response.raise_for_status()
            return {"success": True, "message": f"Bookshelf renamed to '{name}' successfully"}

    async def add_book(
        self,
        title: str,
        author: str,
        bookshelf_id: int,
        isbn: Optional[str] = None,
        cover_url: Optional[str] = None,
    ) -> dict:
        """Add a new book."""
        data = {
            "title": title,
            "author": author,
            "bookshelf_id": str(bookshelf_id),
        }
        if isbn:
            data["isbn"] = isbn
        if cover_url:
            data["cover_url"] = cover_url

        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(BASE_URL, "/books"),
                headers=self.headers,
                data=data,
            )
            response.raise_for_status()
            return {"success": True, "message": f"Book '{title}' by {author} added successfully"}

    async def move_book(self, book_id: int, bookshelf_id: int) -> dict:
        """Move a book to a different bookshelf."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(BASE_URL, f"/books/bookshelves/{bookshelf_id}/assign"),
                headers=self.headers,
                data={"book_id": str(book_id)},
            )
            response.raise_for_status()
            return {"success": True, "message": f"Book moved to bookshelf {bookshelf_id} successfully"}

    async def remove_book(self, bookshelf_id: int, book_id: int) -> dict:
        """Remove a book from a bookshelf."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                urljoin(BASE_URL, f"/books/bookshelves/{bookshelf_id}/remove/{book_id}"),
                headers=self.headers,
            )
            response.raise_for_status()
            return {"success": True, "message": "Book removed from bookshelf successfully"}

    async def change_book_cover(self, bookshelf_id: int, book_id: int, cover_url: str) -> dict:
        """Change the cover for a book."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(BASE_URL, f"/books/bookshelves/{bookshelf_id}/cover/{book_id}"),
                headers=self.headers,
                data={"cover_url": cover_url},
            )
            response.raise_for_status()
            return {"success": True, "message": "Book cover updated successfully"}

    async def get_reading_goals(self) -> dict:
        """Get reading goals."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                urljoin(BASE_URL, "/books/goals"),
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_goal_progress(self, goal_id: int) -> dict:
        """Get books list progress toward a goal."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                urljoin(BASE_URL, f"/books/goals/{goal_id}"),
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_reading_goal(self, goal_id: int, value: int, progress: Optional[int] = None) -> dict:
        """Update reading goal."""
        data = {"value": str(value)}
        if progress is not None:
            data["progress"] = str(progress)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(BASE_URL, f"/books/goals/{goal_id}"),
                headers=self.headers,
                data=data,
            )
            response.raise_for_status()
            return {"success": True, "message": "Reading goal updated successfully"}


def create_server(bearer_token: str) -> FastMCP:
    """Create the FastMCP server."""
    mcp = FastMCP("Micro Books API")
    client = MicroBooksClient(bearer_token)

    @mcp.tool()
    async def get_bookshelves() -> str:
        """Get all bookshelves from Micro.blog."""
        try:
            result = await client.get_bookshelves()
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to get bookshelves")
            raise

    @mcp.tool()
    async def get_bookshelf_books(bookshelf_id: int) -> str:
        """Get books in a specific bookshelf.
        
        Args:
            bookshelf_id: The ID of the bookshelf to get books from
        """
        try:
            result = await client.get_bookshelf_books(bookshelf_id)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to get bookshelf books")
            raise

    @mcp.tool()
    async def add_bookshelf(name: str) -> str:
        """Add a new bookshelf.
        
        Args:
            name: The name of the new bookshelf
        """
        try:
            result = await client.add_bookshelf(name)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to add bookshelf")
            raise

    @mcp.tool()
    async def rename_bookshelf(bookshelf_id: int, name: str) -> str:
        """Rename a bookshelf.
        
        Args:
            bookshelf_id: The ID of the bookshelf to rename
            name: The new name for the bookshelf
        """
        try:
            result = await client.rename_bookshelf(bookshelf_id, name)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to rename bookshelf")
            raise

    @mcp.tool()
    async def add_book(
        title: str,
        author: str,
        bookshelf_id: int,
        isbn: Optional[str] = None,
        cover_url: Optional[str] = None,
    ) -> str:
        """Add a new book.
        
        Args:
            title: The title of the book
            author: The author of the book
            bookshelf_id: The ID of the bookshelf to add the book to
            isbn: The ISBN of the book (optional)
            cover_url: URL to the book cover image (optional)
        """
        try:
            result = await client.add_book(title, author, bookshelf_id, isbn, cover_url)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to add book")
            raise

    @mcp.tool()
    async def move_book(book_id: int, bookshelf_id: int) -> str:
        """Move a book to a different bookshelf.
        
        Args:
            book_id: The ID of the book to move
            bookshelf_id: The ID of the target bookshelf
        """
        try:
            result = await client.move_book(book_id, bookshelf_id)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to move book")
            raise

    @mcp.tool()
    async def remove_book(bookshelf_id: int, book_id: int) -> str:
        """Remove a book from a bookshelf.
        
        Args:
            bookshelf_id: The ID of the bookshelf
            book_id: The ID of the book to remove
        """
        try:
            result = await client.remove_book(bookshelf_id, book_id)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to remove book")
            raise

    @mcp.tool()
    async def change_book_cover(bookshelf_id: int, book_id: int, cover_url: str) -> str:
        """Change the cover for a book.
        
        Args:
            bookshelf_id: The ID of the bookshelf
            book_id: The ID of the book
            cover_url: URL to the new cover image
        """
        try:
            result = await client.change_book_cover(bookshelf_id, book_id, cover_url)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to change book cover")
            raise

    @mcp.tool()
    async def get_reading_goals() -> str:
        """Get reading goals."""
        try:
            result = await client.get_reading_goals()
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to get reading goals")
            raise

    @mcp.tool()
    async def get_goal_progress(goal_id: int) -> str:
        """Get books list progress toward a goal.
        
        Args:
            goal_id: The ID of the reading goal
        """
        try:
            result = await client.get_goal_progress(goal_id)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to get goal progress")
            raise

    @mcp.tool()
    async def update_reading_goal(goal_id: int, value: int, progress: Optional[int] = None) -> str:
        """Update reading goal.
        
        Args:
            goal_id: The ID of the reading goal
            value: The target number of books for the goal
            progress: The current progress (number of books read, optional)
        """
        try:
            result = await client.update_reading_goal(goal_id, value, progress)
            return json.dumps(result, indent=2)
        except Exception:
            logger.exception("Failed to update reading goal")
            raise

    return mcp


def main():
    """Main entry point for the DXT extension."""
    # Get bearer token from environment
    bearer_token = os.environ.get("MICRO_BLOG_BEARER_TOKEN")
    if not bearer_token:
        logger.error("Error: MICRO_BLOG_BEARER_TOKEN environment variable is required")
        sys.exit(1)

    logger.info("Starting Micro.blog Books MCP Server (Python DXT)...")
    
    try:
        # Create and run the server
        app = create_server(bearer_token)
        app.run()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()