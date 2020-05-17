FROM gitpod/workspace-full
                    
USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get update \
    && sudo apt-get install -y software-properties-common \
    && sudo add-apt-repository -y ppa:deadsnakes/ppa \
    && sudo apt-get update \
    && sudo apt-get install -y python3.5 python3.6 python3.7 python3.8 python3.9 tox python3-sphinx

RUN pip install -U pylint pytest mock nose \
    && pip3 install -U pylint pytest mock nose 

#
# More information: https://www.gitpod.io/docs/config-docker/
