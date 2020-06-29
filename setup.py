# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from setuptools import setup
import os
import shutil

if "TRAVIS_BUILD_DIR" in os.environ:
    REQ_PATH = os.getenv("TRAVIS_BUILD_DIR")
elif "TOX_BUILD_DIR" in os.environ:
    REQ_PATH = os.getenv("TOX_BUILD_DIR")
else:
    REQ_PATH = "."

with open(REQ_PATH + "/requirements.txt") as f:
    requirements = f.read().splitlines()

shutil.copyfile(REQ_PATH + "/bin/cli.py", REQ_PATH + "/bin/hpecp")

# make executable
os.chmod(REQ_PATH + "/bin/hpecp", 509)

setup(
    name="hpecp",
    description="HPE Container Platform client",
    author="Chris Snow",
    author_email="chsnow123@gmail.com",
    url="https://github.com/hpe-container-platform-community/hpecp-python-library",
    packages=["hpecp"],
    scripts=["bin/hpecp"],
    keywords="",
    install_requires=requirements,
    test_suite="nose.collector",
    tests_require=["nose", "mock", "mock", "coverage[toml]"],
    classifiers=[
        "License :: OSI Approved :: MIT",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
