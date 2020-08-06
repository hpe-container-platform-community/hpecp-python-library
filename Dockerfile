FROM theiaide/theia-python:latest

COPY requirements.txt /tmp

## User account
RUN adduser --disabled-password --gecos '' theia && \
    adduser theia sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    chown -R theia:theia /home/theia

RUN  apt-get update \
   && apt-get install -y vim yarn \
   && apt-get install -y make build-essential libssl-dev zlib1g-dev \ 
          libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
          libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git \
   && apt-get clean \
   && apt-get auto-remove -y \
   && rm -rf /var/cache/apt/* \
   && rm -rf /var/lib/apt/lists/* 

USER theia
WORKDIR /home/theia

# Python2 and Python3 are installed by parent Dockerfile:
# https://github.com/theia-ide/theia-apps/blob/master/theiaide/theia-python/Dockerfile

# Save the preinstalled python paths - do this before setting up pyenv because pyenv may report
# different binaries with which.

RUN which python > ~/python2_path
RUN which python3 > ~/python3_path

RUN /bin/bash -c " \
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
   && git clone https://github.com/momo-lab/xxenv-latest.git ~/.pyenv/plugins/latest \
   "

RUN echo 'export PYENV_ROOT="~/.pyenv"' >> ~/.bashrc \
   && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
   && echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi' >> ~/.bashrc

RUN cat ~/.bashrc

RUN export PATH=/home/theia/.pyenv/bin:$PATH; \
   eval "$(/home/theia/.pyenv/bin/pyenv init -)"; \
   pyenv latest install 2.7 \
   && pyenv latest install 3.5 \
   && pyenv latest install 3.6 \
   && pyenv latest install 3.7 \
   && pyenv latest install 3.8 \
   && pyenv install 3.9-dev \
   && pyenv local $(pyenv versions --bare) \
   && pyenv versions

# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
#     && sudo python get-pip.py

USER root

RUN echo "Installing python modules" \
    && PY_PATHS=$(ls -1 /home/theia/.pyenv/versions/*/bin/python?.? && cat /home/theia/python3_path && cat /home/theia/python2_path) \
    && PY_PATHS=$(cat /home/theia/python3_path && cat /home/theia/python2_path) \
    && for v in ${PY_PATHS}; do ${v} -m pip install --upgrade pip setuptools wheel; done \
    && for v in ${PY_PATHS}; do ${v} -m pip install --upgrade tox tox-pyenv ipython pylint pytest mock nose flake8 flake8-docstrings autopep8; done \
    && /home/theia/.pyenv/versions/*/bin/python3.8 -m pip install -U black isort python-language-server sphinx\
    && ln -f -s /home/theia/.pyenv/versions/*/bin/black /bin/ \
    && ln -f -s /home/theia/.pyenv/versions/*/bin/isort /bin/ \
    && for v in ${PY_PATHS}; do ${v} -m pip install -r /tmp/requirements.txt; done 

RUN chown -R theia:theia /home/theia 

USER theia
WORKDIR /home/theia

#RUN echo 'PATH=$PATH:/home/theia/.local/bin/' >> /home/theia/.bashrc

ENV PYTHONPATH=/home/project:$PYTHONPATH

