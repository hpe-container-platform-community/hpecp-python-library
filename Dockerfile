FROM theiaide/theia-full:next

COPY requirements.txt /tmp

RUN sudo apt-get update \
    # && sudo apt-get install -y software-properties-common \
    # && sudo add-apt-repository -y ppa:deadsnakes/ppa \
    && sudo apt-get remove --purge -y python \
    && sudo apt-get install -y python-pip python3-pip python3-sphinx vim
    # && sudo apt-get install -y python3.5 python3.6 python3.7 python3.8 python3.9 python3.9-distutils 

RUN sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git \
    && git clone https://github.com/pyenv/pyenv.git /home/theia/.pyenv \
    && git clone https://github.com/momo-lab/xxenv-latest.git /home/theia/.pyenv/plugins/xxenv-latest \
    && echo 'export PYENV_ROOT="/home/theia/.pyenv"' >> /home/theia/.bashrc \
    && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /home/theia/.bashrc \
    && echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi' >> /home/theia/.bashrc

RUN /home/theia/.pyenv/bin/pyenv latest install 2.7 \
    && /home/theia/.pyenv/bin/pyenv latest install 3.5 \
    && /home/theia/.pyenv/bin/pyenv latest install 3.6 \
    && /home/theia/.pyenv/bin/pyenv latest install 3.7 \
    && /home/theia/.pyenv/bin/pyenv latest install 3.8 \
    && /home/theia/.pyenv/bin/pyenv install 3.9-dev \
    && /home/theia/.pyenv/bin/pyenv local $(/home/theia/.pyenv/bin/pyenv versions --bare) \
    && /home/theia/.pyenv/bin/pyenv versions

RUN echo "Installing python modules" \
    && PYENV_PATHS=$(ls -1 /home/theia/.pyenv/versions/*/bin/python?.?) \
    && PYENV_3PATHS=$(ls -1 /home/theia/.pyenv/versions/*/bin/python3.?) \
    && for v in ${PYENV_PATHS}; do ${v} -m pip install --upgrade pip; done \
    && for v in ${PYENV_PATHS}; do ${v} -m pip install -U tox tox-pyenv ipython pylint pytest mock nose flake8-docstrings; done \
    && /home/theia/.pyenv/versions/*/bin/python3.8 -m pip install -U black isort \
    && sudo ln -f -s /home/theia/.pyenv/versions/*/bin/black /bin/ \
    && sudo ln -f -s /home/theia/.pyenv/versions/*/bin/isort /bin/ \
    && for v in ${PYENV_PATHS}; do ${v} -m pip install -r /tmp/requirements.txt; done 

RUN echo 'PATH=$PATH:/home/theia/.local/bin/' >> /home/theia/.bashrc

ENV PYTHONPATH=/home/project:$PYTHONPATH

