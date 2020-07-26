FROM theiaide/theia-full:next

COPY requirements.txt /tmp

RUN sudo apt-get update \
    && sudo apt-get install -y software-properties-common \
    && sudo add-apt-repository -y ppa:deadsnakes/ppa \
    && sudo apt-get update \
    && sudo apt-get install -y python3.5 python3.6 python3.7 python3.8 python3.9 tox python3-sphinx vim

RUN pip install -U pylint pytest mock nose \
    && pip3 install -U pylint pytest mock nose black \
    && pip install -r /tmp/requirements.txt \
    && pip3 install -r /tmp/requirements.txt 

RUN echo 'PATH=$PATH:/home/theia/.local/bin/' > /home/theia/.bash_profile

ENV PYTHONPATH=/home/project:$PYTHONPATH
