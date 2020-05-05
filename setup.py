from setuptools import setup, find_packages

setup(
  name='hpecp',
  description="HPE Container Platform client",
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/hpe-container-platform-community/hpecp-python-library',
  packages = ['hpecp'],
  scripts=['bin/hpecp'],
  keywords = '',
  install_requires=[ 'requests', 'tabulate', 'six', 'enum34; python_version == "2.7"', 'polling' ],
  test_suite='nose.collector',
  tests_require=['nose'],
  classifiers=[
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
  ],
)
