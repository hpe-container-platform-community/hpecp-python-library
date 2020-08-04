### DEVELOPMENT ENVIRONMENT

You can use gitpod - click [here](https://gitpod.io/#https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/DEVELOPING.md) to launch.

- Installing the CLI in gitpod:

```
pip install -e .
source <(hpecp autocomplete bash) # setup autocompletion
hpecp configure-cli
```

### Install from branch

pip install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@branch_name

#### Mock Rest Service

- First, open a terminal, then run:

```
/opt/SoapUI-5.5.0/bin/mockservicerunner.sh -m "REST MockService" tests/HPECP-REST-API-SOAPUI.xml 
```

- Open another terminal and install the CLI (see instructions above)
- Configure the cli:

```
cat > ~/.hpecp.conf <<EOF
[default]
api_host = localhost
api_port = 8080
use_ssl = False
verify_ssl = False
warn_ssl = False
username = admin
password = admin123
EOF
```

- Run the cli: 

```
hpecp license platform-id
```

- You can check the log in the SOAP UI terminal window, e.g.

```
...
14:33:30,558 INFO  [SoapUIMockServiceRunner] Handled request 1; [/api/v1] with [Login Success] in [0ms] at [2020-06-06 14:33:29.807]
14:33:30,565 INFO  [SoapUIMockServiceRunner] Handled request 2; [/api/v1] with [License] in [0ms] at [2020-06-06 14:33:30.563]
```

- The following mock responses have been defined:
  - `POST /api/v1/login` (create session)
  - `GET /api/v1/license` (list licenses)
  - `GET /api/v1/role` (list roles)
  - `GET /api/v1/role/1` (returns role 1)
  - `GET /api/v1/role/99` (returns HTTP 404 - not found)


### DOCS

#### format

Numpy docstring format are required: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard

Docstring formatting is verified with flake8 as Travis build step.

#### Building

In the Gitpod Terminal:

```
cd docs/
make clean && make html
open build/html/index.html # (right click and preview file)
```

### Testing

#### GUI

In Gitpod IDE:

- Click `View Menu -> Tests`
- Right Click `TEST` and select `PYTHON`
- Click the `Circular Arrow` to find tests
- Click the `Play Button` to test

NOTE: click the `Python version` in the IDE footer bar to chose a different python version and repeat above steps.

#### Terminal

Run all tests **for all python versions** declared in tox.ini

```
tox
```

Run just the Python 2.7 tests

```
tox -e py27
```

Run all tests in a specific file:

```
tox -e py27 -- tests/library/client_test.py
```

Run a single test

```
tox -e py27 -- tests/library/client_test.py:TestCreateFromProperties.test_create_from_config_file_factory_method
```

### COVERAGE

Aim for 100% test coverage to ensure library will work with all specified python versions.

```
coverage erase && coverage run --source hpecp,bin setup.py test && coverage report -m
```

### CODE QUALITY

```
pip3 install flake8 flake8-docstrings
flake8 --docstring-convention numpy bin/ hpecp/
flake8 --ignore=D tests/
```

### FORMATTING

```
pip3 install black
# automatically format hpecp folder
black hpecp 
```

### RELEASING

 - Not applicable while pre-alpha.

```
vi setup.py # increment version
git add ...
git commit -m '...'
git tag 0.0.9  -m "Add pypi python versions"
git push origin 0.0.9 
python setup.py sdist upload -r pypi
```

### TROUBLESHOOTING

If you are unable to push from gitpod, naviate to: https://gitpod.io/access-control/

Ensure you select:

- write public repos
- read organisations

Click Update and authorize on the gitpub page that opens.
