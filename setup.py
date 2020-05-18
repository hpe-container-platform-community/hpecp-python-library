from setuptools import setup, find_packages
import os
import shutil

if 'TRAVIS_BUILD_DIR' in os.environ:
    REQ_PATH=os.getenv('TRAVIS_BUILD_DIR')
elif 'TOX_BUILD_DIR' in os.environ:
    REQ_PATH=os.getenv("TOX_BUILD_DIR")
else:
    REQ_PATH='.'

with open(REQ_PATH + '/requirements.txt') as f:
    requirements = f.read().splitlines()

shutil.copyfile(
  REQ_PATH + './bin/cli.py', 
  REQ_PATH + './bin/hpecp'
  )

setup(
  name='hpecp',
  description="HPE Container Platform client",
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/hpe-container-platform-community/hpecp-python-library',
  packages = ['hpecp'],
  scripts=['bin/hpecp'],
  keywords = '',
  install_requires=requirements,
  test_suite='nose.collector',
  tests_require=['nose','mock'],
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
