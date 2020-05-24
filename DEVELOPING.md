### DEVELOPMENT ENVIRONMENT

You can use gitpod - click [here](https://gitpod.io/#https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/DEVELOPING.md) to launch.

- Installing the CLI in gitpod:

```
pip install -e . && hpecp autocomplete bash > hpecp-bash.rc && source hpecp-bash.rc
hpecp gateway states
```

#### BUILDING DOCS

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
coverage erase && coverage run --source hpecp setup.py test && coverage report -m
```


### FORMATTING

Currently not used

```
autopep8 --in-place --aggressive --recursive hpecp/
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
