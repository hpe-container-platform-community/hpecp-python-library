from setuptools import setup, find_packages

setup(
  name='hpecp',
  description="HPE Container Platform library",
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/hpe-container-platform-community/hpecp-python-library',
  packages = ['hpecp'],
  keywords = '',
  install_requires=[ 'requests' ],
  test_suite='nose.collector',
  tests_require=['nose'],
  classifiers=[
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
  ],
)
