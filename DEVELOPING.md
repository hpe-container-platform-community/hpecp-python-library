### DEVELOPMENT ENVIRONMENT

I use Theia IDE for development. 

I use Theia because it is easy to provide all the dependencies out of the box.

To startup Theia:

```
./run_ide.sh 
```

Then open browser to http://localhost:3000

### REFERENCE IMPLEMENTATION

 - [k8s_cluster code](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/hpecp/k8s_cluster.py)
 - [k8s_cluster tests](https://github.com/hpe-container-platform-community/hpecp-python-library/blob/master/tests/library/k8s_cluster_test.py)

### COVERAGE

Aim for 100% test coverage to ensure library will work with all specified python versions.

#### BUILDING DOCS

```
sudo pip install -e
sudo pip3 install -e .

cd docs/
make clean && make html
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

Run all tests **for all python versions** declared in tox.ini

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
