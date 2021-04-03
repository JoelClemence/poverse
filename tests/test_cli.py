from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from poverse.cli import cli
from poverse.exceptions import LockFileException


@pytest.fixture()
def cli_runner():
    return CliRunner()


@pytest.fixture()
def get_installed_version_mock():
    with patch("poverse.cli.get_installed_version") as mock:
        yield mock


def test_error_exit_code_when_no_package_supplied(
    cli_runner: CliRunner, get_installed_version_mock
):
    assert cli_runner.invoke(cli).exit_code != 0


def test_status_code_zero_when_only_package_name_supplied(
    cli_runner: CliRunner, get_installed_version_mock
):
    assert cli_runner.invoke(cli, ["-p", "myawesomepackage"]).exit_code == 0


def test_gets_installed_version_of_package_supplied(
    cli_runner: CliRunner, get_installed_version_mock
):
    cli_runner.invoke(cli, ["-p", "myawesomepackage"])

    get_installed_version_mock.assert_called_once_with(
        "myawesomepackage", f"{Path.cwd()}/poetry.lock"
    )


def test_echos_version_of_package_supplied(
    cli_runner: CliRunner, get_installed_version_mock
):
    get_installed_version_mock.return_value = "0.1.1"

    result = cli_runner.invoke(cli, ["-p", "myawesomepackage"])

    assert "0.1.1" == result.output.strip()


def test_returns_error_exit_code_when_exception_raised(
    cli_runner: CliRunner, get_installed_version_mock
):
    get_installed_version_mock.side_effect = LockFileException(
        "Lock file not in supported format"
    )

    assert cli_runner.invoke(cli, ["-p", "myawesomepackage"]).exit_code != 0


def test_gets_value_of_package_from_supplied_lock_file(
    cli_runner: CliRunner, get_installed_version_mock
):
    test_lock_file_path = f"{Path.cwd()}/tests/test_data/poetry.lock"

    cli_runner.invoke(cli, ["-p", "myawesomepackage", test_lock_file_path])

    get_installed_version_mock.assert_called_once_with(
        "myawesomepackage", test_lock_file_path
    )
