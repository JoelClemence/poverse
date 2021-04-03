# poverse: Gets the version of dependencies installed by Poetry

[Poetry](https://python-poetry.org/) is a great tool for managing python projects. This small library retrieves the version of an installed package.

Supports python versions >=3.7, <=3.9

[![.github/workflows/ci.yaml](https://github.com/JoelClemence/poverse/actions/workflows/ci.yaml/badge.svg)](https://github.com/JoelClemence/poverse/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/poverse.svg)](https://pypi.org/project/poverse/)

## Installation

```sh
$ pip install poverse
```

## Usage

### Cli

```bash
$ poverse --help
Usage: poverse [OPTIONS] [LOCK_FILE_PATH]

  Looks for package with name in LOCK_FILE_PATH.

  LOCK_FILE_PATH is the path to Poetry lock file defaults to
  `$PWD/poetry.lock` if not supplied

Options:
  -p, --package TEXT  Name of the package in lock file  [required]
  --help              Show this message and exit.
```

#### Example usage

```sh
$ poverse -p click
7.1.2

$ poverse -p click $PWD/tests/test_data/poetry.lock
7.1.2
```

### API

**`get_installed_version`**

Gets the actual installed version for the supplied package with name
from the poetry lock.

**Params:**
- `package_name` (_**required**, str_): name of the package that could be in the lock file (required)
- `lock_file_path` (_str_): path to `poetry.lock` file. Defaults to a `poetry.lock` in the current directory.

**Returns:** _Optional[str]_ - Version of requested dependency, `None` if package does not exist.

#### Examples

```python
from poverse import get_installed_version

get_installed_version("boto3") # Get the installed version of boto3 from project's poetry.lock

get_installed_version("boto3", "/home/user/projects/project/poetry.lock") # Get the installed version of boto3 from the poetry lock supplied
```

## Motivation

The idea behind this project is for applications where you perhaps need to install specific versions of binaries (e.g. Spark or GDAL) that are dependent on your application dependencies.

## Development

Found something that should not be happening? Do you have an idea that would make this library great? Raise an issue or PR, contributions welcome!
