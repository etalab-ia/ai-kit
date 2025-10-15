"""Main CLI entry point for ai-kit."""

import click

from ai_kit.cli.commands import notebook


@click.group()
@click.version_option()
def cli():
    """AI-Kit CLI - Command-line tools for French Government AI services."""
    pass


# Register command groups
cli.add_command(notebook.notebook)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
