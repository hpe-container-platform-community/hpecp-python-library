FROM theiaide/theia-full:next

COPY requirements.txt /tmp

RUN sudo apt-get update \
    && sudo apt-get install -y software-properties-common \
    && sudo add-apt-repository -y ppa:deadsnakes/ppa \
    && sudo apt-get update \
    && sudo apt-get install -y python3.5 python3.6 python3.7 python3.8 python3.9 tox python3-sphinx python-pip python3-pip python3.9-distutils vim

# FIXME: Python 3.9 returns errors with pip
RUN echo "Installing python modules" \
    && for v in 2 3 3.5 3.6 3.7 3.8; do python${v} -m pip install -U pylint pytest mock nose flake8-docstrings flake8-per-file-ignores==0.8.1; done \
    && for v in 3 3.5 3.6 3.7 3.8; do python${v} -m pip install -U black; done \
    && sudo ln -s /home/theia/.local/bin//black /bin/ \
    && for v in 2 3 3.5 3.6 3.7 3.8; do python${v} -m pip install -r /tmp/requirements.txt; done 

RUN echo 'PATH=$PATH:/home/theia/.local/bin/' >> /home/theia/.bashrc

ENV PYTHONPATH=/home/project:$PYTHONPATH