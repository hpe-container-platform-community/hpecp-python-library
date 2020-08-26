FROM gitpod/workspace-full

USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get -q update && sudo apt-get install -y shellcheck tox python3-sphinx python3-pip

ENV PATH=$PATH:/home/gitpod/.local/bin

# setup the gitpod bundled python
RUN /home/gitpod/.pyenv/versions/2.7.*/bin/python2 -m pip install --upgrade pip
RUN /home/gitpod/.pyenv/versions/3.8.*/bin/python3 -m pip install --upgrade pip

# additional python versions
RUN pyenv install 3.5.9
RUN pyenv install 3.6.9
RUN pyenv install 3.7.7

# The following fails: build failed: cannot build base image: The command '/bin/sh -c pyenv install 3.9-dev' returned a non-zero code: 1
# RUN pyenv install 3.9-dev

# Allow pytest to discover tests
RUN echo 'PYTHONPATH=/workspace/hpecp-python-library:$PYTHONPATH' > ~/.bashrc.d/40-pythonpath

RUN \
    wget https://s3.amazonaws.com/downloads.eviware/soapuios/5.5.0/SoapUI-5.5.0-linux-bin.tar.gz \
    && sudo tar -xzf SoapUI-5.5.0-linux-bin.tar.gz -C /opt/ \
    && rm SoapUI-5.5.0-linux-bin.tar.gz \
    && sudo rm /opt/SoapUI-5.5.0/lib/groovy-all-2.4.4.jar \
    && ( \
       cd /tmp \
       && wget https://dl.bintray.com/groovy/maven/apache-groovy-binary-2.4.19.zip \
       && unzip /tmp/apache-groovy-binary-2.4.19.zip \
       && sudo cp groovy-2.4.19/embeddable/groovy-all-2.4.19.jar /opt/SoapUI-5.5.0/lib/ \
       )
#
# More information: https://www.gitpod.io/docs/config-docker/
