If you are developing this HPECP library, you can run the scripts directly against your source code folders with:

```shell
export PYTHONPATH=.:$PYTHONPATH
./docs/scripts/license_get.py
```

Other users should install the library to use these scripts:

```shell
pip install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master
```