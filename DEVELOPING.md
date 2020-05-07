### DEVELOPMENT ENVIRONMENT

I use Theia for development. Startup:

```
./run_ide.sh 
```

Then open browser to http://localhost:3000

Inside the Theia terminal:

```
# install python versions for tox
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.5 python3.6 python3.7 python3.8

# install tox
sudo apt install tox
```


### COVERAGE

Aim for 100% test coverage to ensure library will work with all specified python versions.

### FORMATTING

Currently not used

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
python setup.py test
python3 setup.py test
```

Run all tests with coverage output:

```
coverage erase && coverage run --source hpecp setup.py test && coverage report -m
```

#### Using tox for testing

Run all tests for all python versions in tox.ini

```
tox
```

```
tox -e py27
```

Run all tests in a file:

```
tox -e py27 -- tests/library/client_test.py
```

Run a single test

```
tox -e py27 -- tests/library/client_test.py:TestCreateFromProperties.test_create_from_config_file_factory_method
```
