FROM gitpod/workspace-full
                    
USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get update \
    && sudo apt-get install -y tox python3-sphinx python3-pip

ENV PYTHONPATH=/workspace/hpecp-python-library:$PYTHONPATH
#
# More information: https://www.gitpod.io/docs/config-docker/
