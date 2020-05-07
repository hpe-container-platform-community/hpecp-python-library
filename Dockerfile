FROM theiaide/theia-full:next

RUN sudo apt-get update \
    && sudo apt-get install -y software-properties-common

RUN sudo add-apt-repository -y ppa:deadsnakes/ppa
RUN sudo apt-get update 
RUN sudo apt-get install -y python3.5 python3.6 python3.7 python3.8 tox
