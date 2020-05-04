### DEVELOPMENT ENVIRONMENT

I use Visual Studio Code for development.

### COVERAGE

Aim for 100% test coverage to ensure library will work with all specified python versions.

### FORMATTING

```
autopep8 --in-place --aggressive --recursive hpecp/
```

#### BUILDING DOCS

```
cd docs/
make clean html
open build/html/index.html
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
### Testing

Run all tests:

```
tox -e py27
```

Run all tests with coverage output:

```
coverage erase && coverage run --source hpecp setup.py test && coverage report -m
```

Run a single test.

```
pytest tests/doc/test_create_cluster.py
```

Or, with tox:

```
tox -e py27 -- tests/doc/test_list_orgs_and_spaces.py
```

Or:

```
tox -e py27 -- tests/doc/test_list_orgs_and_spaces.py:DocExampleScripts_Test.test
```
