# py-pytest-task

This is a test-ware to practice performing API tests using Python's pytest and requests library.

## Prerequisites

In order to execute the implemented test cases, an account is needed on the https://www.spotify.com/.
If the account is created the OAuth Key and User ID should be added to the [constants](constants.py) instead of the {YOUR_OAUTH_TOKEN} and {YOUR_USER_ID} as a string.

1. Python 3.9+
1. Pip
1. pytest 6.2.2
1. requests 2.25.0
1. jsonschema 3.2.0

## Framework used

| Framework | Documentation                                                                                                             |
|:----------|:--------------------------------------------------------------------------------------------------------------------------|
| pytest    | [pytest](https://docs.pytest.org/en/stable/index.html) is a framework that makes building simple and scalable tests easy. |
| requests  | [Requests](https://pypi.org/project/requests/) is a simple, yet elegant HTTP library.                                     |
| jsonschema | [jsonschema](https://pypi.org/project/jsonschema/) is an implementation of JSON Schema validation for Python. |

## Test cases

The implemented test cases can be found in [API.md](test_cases/API.md).

## Setup

```shell
pip install -r requirements.txt
```

## Execution
To execute all the test cases:
```shell
pytest
```

To execute one test module:
```shell
pytest test/test_get.py::TestGetMethod
```

To execute one test function:
```shell
pytest test/test_get.py::TestGetMethod::test_get_status_code
```