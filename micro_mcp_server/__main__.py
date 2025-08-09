"""Main entry point for the Micro.blog Books MCP Server."""

import sys

import click

from .server import create_server


@click.command()
@click.option(
    "--bearer-token",
    envvar="MICRO_BLOG_BEARER_TOKEN",
    required=True,
    help="Bearer token for Micro.blog API (can also be set via MICRO_BLOG_BEARER_TOKEN env var)",
)
def main(bearer_token: str) -> None:
    """Run the Micro.blog Books MCP Server."""
    if not bearer_token:
        click.echo("Error: Bearer token is required", err=True)
        click.echo("Set MICRO_BLOG_BEARER_TOKEN environment variable or use --bearer-token option", err=True)
        sys.exit(1)

    app = create_server(bearer_token)
    app.run()


if __name__ == "__main__":
    main()