import click

from . import DEFAULT_POETRY_LOCK_FILE, get_installed_version
from .exceptions import LockFileException


@click.argument("lock_file_path", default=DEFAULT_POETRY_LOCK_FILE)
@click.option("--package", "-p", required=True, help="Name of the package in lock file")
@click.command("poverse")
def cli(package: str, lock_file_path: str):
    """
    Looks for package with name in LOCK_FILE_PATH.

    LOCK_FILE_PATH is the path to Poetry lock file
    defaults to `$PWD/poetry.lock` if not supplied
    """
    try:
        click.echo(get_installed_version(package, lock_file_path))
    except LockFileException as lock_file_exception:
        raise click.ClickException(
            f"Could not load lock file: {str(lock_file_exception)}"
        )


if __name__ == "__main___":
    cli()
