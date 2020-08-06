ARG NODE_VERSION=10
FROM node:${NODE_VERSION}

COPY requirements.txt /tmp

USER root

# Python2 and Python3 are installed by parent Dockerfile:
# https://github.com/theia-ide/theia-apps/blob/master/theia-full-docker/Dockerfile

# Save the preinstalled python paths - do this before setting up pyenv because pyenv may report 
# different binaries with which.

RUN which python > ~/python2_path
RUN which python3 > ~/python3_path

RUN  apt-get update \
   &&  apt-get install -y vim yarn \
   &&  apt-get install -y make build-essential libssl-dev zlib1g-dev \ 
          libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
          libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git \
   && apt-get clean \
   && apt-get auto-remove -y \
   && rm -rf /var/cache/apt/* \
   && rm -rf /var/lib/apt/lists/* 

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
   && git clone https://github.com/momo-lab/xxenv-latest.git ~/.pyenv/plugins/latest \
   && echo 'export PYENV_ROOT="~/.pyenv"' >> ~/.bashrc \
   && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
   && echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi' >> ~/.bashrc

RUN   /root/.pyenv/bin/pyenv latest install 2.7 \
   && /root/.pyenv/bin/pyenv latest install 3.5 \
   && /root/.pyenv/bin/pyenv latest install 3.6 \
   && /root/.pyenv/bin/pyenv latest install 3.7 \
   && /root/.pyenv/bin/pyenv latest install 3.8 \
   && /root/.pyenv/bin/pyenv install 3.9-dev \
   && /root/.pyenv/bin/pyenv local $(/root/.pyenv/bin/pyenv versions --bare) \
   && /root/.pyenv/bin/pyenv versions

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py

RUN echo "Installing python modules" \
    && PY_PATHS=$(ls -1 ~/.pyenv/versions/*/bin/python?.? && cat ~/python3_path && cat ~/python2_path) \
    && PY_PATHS=$(cat ~/python3_path && cat ~/python2_path) \
    && for v in ${PY_PATHS}; do ${v} -m pip install --upgrade pip setuptools wheel; done \
    && for v in ${PY_PATHS}; do ${v} -m pip install --upgrade tox tox-pyenv ipython pylint pytest mock nose flake8 flake8-docstrings autopep8; done \
    && ~/.pyenv/versions/*/bin/python3.8 -m pip install -U black isort python-language-server sphinx\
    && ln -f -s ~/.pyenv/versions/*/bin/black /bin/ \
    && ln -f -s ~/.pyenv/versions/*/bin/isort /bin/ \
    && for v in ${PY_PATHS}; do ${v} -m pip install -r /tmp/requirements.txt; done 

#RUN echo 'PATH=$PATH:/home/theia/.local/bin/' >> /home/theia/.bashrc

ENV PYTHONPATH=/home/project:$PYTHONPATH

RUN mkdir -p /home/theia \
    && mkdir -p /home/project
WORKDIR /home/theia

ARG version=latest
ADD $version.package.json ./package.json
ARG GITHUB_TOKEN
RUN yarn --cache-folder ./ycache && rm -rf ./ycache && \
     NODE_OPTIONS="--max_old_space_size=4096" yarn theia build ; \
    yarn theia download:plugins
EXPOSE 3000
ENV SHELL=/bin/bash \
    THEIA_DEFAULT_PLUGINS=local-dir:/home/theia/plugins
ENTRYPOINT [ "yarn", "theia", "start", "/home/project", "--hostname=0.0.0.0" ]
