import click
from main import create_app
import pytest
import os
import config.database

# Define custom commands
@click.command()
def run_debug():
    """Run the app in debug mode."""
    os.environ["DATABASE_URI"] = config.database.DATABASE_URI
    os.environ["IS_DEBUG"] = 'TRUE'

    app = create_app()
    app.run(debug=True)

@click.command()
def run_production():
    """Run the app in production mode."""
    os.environ["DATABASE_URI"] = config.database.DATABASE_URI
    os.environ["IS_DEBUG"] = 'FALSE'
    
    app = create_app()
    app.run(debug=False)

@click.command()
def make_build():
    """Build the app (add your build logic here)."""
    raise NotImplementedError()
    click.echo("Building the app...")

@click.command()
def run_tests():
    """Run tests using pytest."""
    os.environ["DATABASE_URI"] = config.database.TESTING_DATABASE_URI

    pytest.main(["-W", "ignore::DeprecationWarning"])

@click.group()
def cli():
    pass

cli.add_command(run_debug)
cli.add_command(run_production)
cli.add_command(run_tests)

if __name__ == '__main__':
    cli()
