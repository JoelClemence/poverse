from io import StringIO
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from poverse import get_installed_version
from poverse.exceptions import LockFileException

with open(f"{Path.cwd()}/tests/test_data/poetry.lock") as test_poetry_lock:
    poetry_lock_content = "\n".join(test_poetry_lock.readlines())


@pytest.fixture()
def open_mock():
    with patch("builtins.open", mock_open(read_data=poetry_lock_content)) as mock:
        yield mock


@pytest.fixture()
def bad_poetry_lock_file():
    with patch("builtins.open", mock_open(read_data="\n")) as mock:
        yield mock


@pytest.fixture()
def missing_name_and_version_lock_file():
    with patch(
        "builtins.open",
        mock_open(read_data=("[[package]]\n" "invalid = true\n" 'name = "package"\n')),
    ) as mock:
        yield mock


def test_get_installed_version_returns_version_of_existing_package(open_mock):
    result = get_installed_version("click", f"{Path.cwd()}/tests/test_data/poetry.lock")

    assert result == "7.1.2"


def test_get_installed_version_returns_none_when_package_not_found(open_mock):
    result = get_installed_version(
        "not-found", f"{Path.cwd()}/tests/test_data/poetry.lock"
    )

    assert result is None


def test_get_installed_version_uses_default_lock_file_when_lock_supplier_not_supplied(
    open_mock,
):
    get_installed_version("package")

    open_mock.assert_called_once_with(f"{Path.cwd()}/poetry.lock")


def test_get_installed_version_raises_exception_when_not_lock_file(
    bad_poetry_lock_file,
):
    __assert_raises_lock_file_exception(
        lambda: get_installed_version(
            "package", f"{Path.cwd()}/tests/test_data/poetry.lock"
        )
    )


def test_get_installed_version_raises_exception_when_lock_file_not_found(open_mock):
    __assert_raises_lock_file_exception(
        lambda: get_installed_version("package", "/not/found/poetry.lock")
    )


def test_get_installed_version_raises_exception_when_package_is_invalid(open_mock):
    invalid_packages = [
        None,
        "",
        " \n\t",
    ]

    for package in invalid_packages:
        __assert_raises_lock_file_exception(
            lambda: get_installed_version(
                package, f"{Path.cwd()}/tests/test_data/poetry.lock"
            )
        )


def test_get_installed_version_raises_exception_when_package_does_not_have_version(
    missing_name_and_version_lock_file,
):
    __assert_raises_lock_file_exception(
        lambda: get_installed_version(
            "package", f"{Path.cwd()}/tests/test_data/poetry.lock"
        )
    )


def __assert_raises_lock_file_exception(fn_call):
    try:
        fn_call()
        raise AssertionError("Should have raised exception")
    except LockFileException:
        pass
    except Exception:
        raise
