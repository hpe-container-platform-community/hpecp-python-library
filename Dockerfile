FROM theiaide/theia-python:latest

ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /tmp

RUN  apt-get update \
   && apt-get install -y vim yarn sudo python3-sphinx \
   && apt-get install -y make build-essential libssl-dev zlib1g-dev \ 
          libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
          libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git \
   && apt-get clean \
   && apt-get auto-remove -y \
   && rm -rf /var/cache/apt/* \
   && rm -rf /var/lib/apt/lists/* 

## User account
RUN adduser --disabled-password --gecos '' theia && \
    adduser theia sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    chown -R theia:theia /home/theia && \
    chmod 777 /home/theia 

RUN echo "Installing python modules in system python versions" \
    && PY_PATHS="/usr/bin/python /usr/bin/python3 and /usr/local/bin/python3" \
    && for v in ${PY_PATHS}; do echo "******* ${v} *******"; ${v} -m pip install --upgrade pip setuptools wheel; done \
    && for v in ${PY_PATHS}; do echo "******* ${v} *******"; ${v} -m pip install --upgrade tox tox-pyenv ipython pylint pytest mock nose flake8 flake8-docstrings autopep8 jmespath fire jinja2; done \
    && for v in ${PY_PATHS}; do ${v} -m pip install -r /tmp/requirements.txt; done \
    && /usr/local/bin/python3 -m pip install -U black isort \
    && ln -f -s /usr/local/bin/black /bin/ \
    && ln -f -s /usr/local/bin/isort /bin/ 

# Setup ssh for git
RUN test -d /home/theia/.ssh || mkdir /home/theia/.ssh \
    && chmod 700 /home/theia/.ssh \
    && touch /home/theia/.ssh/known_hosts \
    && chmod 644 /home/theia/.ssh/known_hosts \
    && chown -R theia /home/theia/.ssh \
    && echo "github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==" > /home/theia/.ssh/known_hosts

USER theia
WORKDIR /home/theia

RUN /bin/bash -c " \
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
   && git clone https://github.com/momo-lab/xxenv-latest.git ~/.pyenv/plugins/latest \
   && git clone https://github.com/doloopwhile/pyenv-register.git ~/.pyenv/plugins/pyenv-register"

RUN echo 'export PYENV_ROOT="/home/theia/.pyenv"' >> ~/.bashrc \
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
   && pyenv register /usr/bin/python \
   && pyenv register /usr/bin/python3 \
   && pyenv register /usr/local/bin/python3 \
   && pyenv local $(pyenv versions --bare) \
   && pyenv versions

RUN echo "Installing python modules in pyenv python versions" \
    && PY_PATHS=$(ls -1 /home/theia/.pyenv/versions/[0-9]*/bin/python?.?) \
    && for v in ${PY_PATHS}; do echo "******* ${v} *******"; ${v} -m pip install --upgrade pip setuptools wheel; done \
    && for v in ${PY_PATHS}; do echo "******* ${v} *******"; ${v} -m pip install --upgrade tox tox-pyenv ipython pylint pytest mock nose flake8 flake8-docstrings autopep8 jmespath fire jinja2; done \
    && for v in ${PY_PATHS}; do ${v} -m pip install -r /tmp/requirements.txt; done 


WORKDIR /home/theia


ENV PYTHONPATH=/home/project:$PYTHONPATH

