from pathlib import Path
from typing import Any, Callable, Dict, Optional

import toml

from .exceptions import LockFileException

DEFAULT_POETRY_LOCK_FILE = f"{Path.cwd()}/poetry.lock"


def get_installed_version(
    package_name: str, lock_file_path: str = DEFAULT_POETRY_LOCK_FILE
) -> Optional[str]:
    """
    Gets the actual installed version for the supplied package with name
    from the poetry lock.

    Params:
        package_name: name of the package that could be in the lock file (required)
        lock_file_path: path to `poetry.lock` file. Defaults to a `poetry.lock` in
            the current directory.
    """
    __validate_args(package_name, lock_file_path)

    try:
        dependencies = __load_dependencies(lock_file_path)

        return dependencies[package_name] if package_name in dependencies else None
    except KeyError:
        raise LockFileException("Lock file format not recognised")


def __load_dependencies(lock_file_path: str) -> Dict[str, str]:
    with open(lock_file_path) as poetry_lock:
        lock_file = toml.load(poetry_lock)

        if "package" not in lock_file:
            raise LockFileException("Lock file format not recognised")

        return {package["name"]: package["version"] for package in lock_file["package"]}


def __validate_args(package_name: str, lock_file_path: str):
    if not package_name or not package_name.strip():
        raise LockFileException("Package name should not be empty or None")

    if not Path(lock_file_path).exists():
        raise LockFileException("Lock file does not exist")
