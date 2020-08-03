Installing the CLI on HPE Container Platform Centos/Redhat Hosts
---

There is an [issue](https://github.com/hpe-container-platform-community/hpecp-python-library/issues/45)
with the version of Python installed by default on HPE CP.

For demo environments, you can workaround this using pyenv:

```
sudo yum install -y  gcc gcc-c++ make git patch openssl-devel zlib zlib-devel readline-devel sqlite-devel bzip2-devel libffi-devel
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.6.10

git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv virtualenv 3.6.10 my-3.6.10
pyenv activate my-3.6.10

pip install -U hpecp
```

Whenever you run the hpecp cli activate python 3.6.10 first, I.e.

```
pyenv activate my-3.6.10
hpecp do_something 
```
