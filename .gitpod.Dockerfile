FROM gitpod/workspace-full

USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*

# setup the gitpod bundled python
RUN pyenv shell 2.7.17 && pip install -U pytest mock awscli -r ./requirements.txt --user
RUN pyenv shell 3.8.2 && pip3 install -U pytest tox mock awscli black flake8 -r ./requirements.txt --user

# additional python versions
RUN pyenv install 3.5.9   && pyenv shell 3.5.9   && pip3 install -U pytest mock awscli flake8 -r ./requirements.txt --user
RUN pyenv install 3.6.9   && pyenv shell 3.6.9   && pip3 install -U pytest mock awscli black flake8 -r ./requirements.txt --user
RUN pyenv install 3.7.7   && pyenv shell 3.7.7   && pip3 install -U pytest mock awscli black flake8 -r ./requirements.txt --user
RUN pyenv install 3.9-dev && pyenv shell 3.9-dev && pip3 install -U pytest mock awscli black flake8 -r ./requirements.txt --user

ENV PYTHONPATH=/workspace/hpecp-python-library:$PYTHONPATH
#
# More information: https://www.gitpod.io/docs/config-docker/
