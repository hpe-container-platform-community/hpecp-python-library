Installing on HPE CP Centos/Redhat Hosts
---

There is an [issue](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/45)
with the version of Python installed by default on HPE CP.

For demo environments, you can workaround this using pyenv:

```
sudo yum install -y  gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> .bashrc
echo 'eval "$(pyenv init -)"' >> .bashrc
source .bashrc
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo ‘eval “$(pyenv virtualenv-init -)“’ >> ~/.bash_profile
source ~/.bash_profile
pyenv virtualenv 3.7.7
pyenv activate 3.7.7
pip install --upgrade git+https://github.com/hpe-container-platform-community/hpecp-client@master
```

Whenever you run the hpecp cli activate python 3.7.7 first, I.e.

```
pyenv activate 3.7.7
hpecp do_something 
```
