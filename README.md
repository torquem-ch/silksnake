# Silksnake

Python library to access [Turbo-Geth](https://github.com/ledgerwatch/turbo-geth)/[Silkworm](https://github.com/torquem-ch/silkworm) data remotely.

[![CircleCI](https://circleci.com/gh/torquem-ch/silksnake.svg?style=shield)](https://circleci.com/gh/torquem-ch/silksnake)
[![CodeCov](https://codecov.io/gh/torquem-ch/silksnake/branch/master/graph/badge.svg)](https://codecov.io/gh/torquem-ch/silksnake)
[![License](https://img.shields.io/github/license/torquem-ch/silksnake?color=important)](https://img.shields.io/github/license/torquem-ch/silksnake)
![version](https://img.shields.io/github/v/release/torquem-ch/silksnake?sort=semver)
![semver](https://img.shields.io/badge/semver-2.0.0-blue)

<br>

## Platform Requirements

### Python Interpreter
Install __Python 3.x__ from [here](https://www.python.org/downloads/) and check the installation using

```shell-session
$ python --version
Python 3.6.9
```

### Python Package Installer (pip)
After Python installation, it is recommended [Upgrading pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip)


## Structure
The project is organized in the following folders:
- __docs__ contains the programming guide of Silksnake and the user guide of Silksnake tools
- __silksnake__ contains the Silksnake source code
- __tests__ contains the unit and integration tests
- __tools__ contains the Silksnake command-line tools for accessing TurboGeth/Silksworm data using Key-Value (KV) I/F


## Setup
Please perform the following commands from silksnake root folder.

### Dependencies
Install dependencies using

```shell-session
$ pip install -r requirements.txt
```

or

```shell-session
$ python setup.py
```

### Test
Run unit tests using

```shell-session
$ pytest
```

### Coverage
Run test coverage using

```shell-session
$ coverage run -m pytest
$ coverage report
```

### Linter
Run [pylint](https://www.pylint.org/) using

```shell-session
$ pylint silksnake tests tools
```

### Binding Generation (not required)
Run binding generation for turbo-geth/silkworm KV gRPC interface using

```shell-session
$ python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. silksnake/remote/proto/kv.proto
```
