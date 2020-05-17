FROM gitpod/workspace-full
                    
USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*

RUN \
    sudo apt-get update \
    && sudo apt-get install -y tox python3-sphinx python3-pip

RUN \
  pyenv install 2.7.17 \
  && pyenv install 3.5.9 \
  && pyenv install 3.6.9 \
  && pyenv install 3.7.7 \
  && pyenv install 3.8.2 \
  && pyenv install 3.9-dev \
  && pyenv global 2.7.17 3.5.9 3.6.9 3.7.7 3.8.2 3.9-dev \
  && pip install --upgrade pip

RUN \
  pip3 install -U pytest --user \
  && pip3 install -U pylint --user

ENV PYTHONPATH=/workspace/hpecp-python-library:$PYTHONPATH
#
# More information: https://www.gitpod.io/docs/config-docker/
