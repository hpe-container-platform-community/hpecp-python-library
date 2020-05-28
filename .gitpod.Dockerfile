FROM gitpod/workspace-full

USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get -q update && sudo apt-get install -y shellcheck tox python3-sphinx 

ENV PATH=$PATH:/home/gitpod/.local/bin

# setup the gitpod bundled python
RUN /home/gitpod/.pyenv/versions/2.7.17/bin/python2 -m pip install --upgrade pip
RUN /home/gitpod/.pyenv/versions/3.8.2/bin/python3 -m pip install --upgrade pip

# additional python versions
RUN pyenv install 3.5.9
RUN pyenv install 3.6.9
RUN pyenv install 3.7.7
RUN pyenv install 3.9-dev

ENV PYTHONPATH=/workspace/hpecp-python-library:$PYTHONPATH
#
# More information: https://www.gitpod.io/docs/config-docker/
