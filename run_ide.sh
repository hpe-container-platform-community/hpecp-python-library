#!/usr/bin/env bash

IMG=hpecp/hpecp-ide:latest

if [[ "$(docker images -q $IMG 2> /dev/null)" == "" ]]; then
  ./build_ide.sh
fi

echo

git_vars=1
if [[ -z $GIT_USER ]]; then
  echo "GIT_USER variable not found"
  git_vars=0 
fi

if [[ -z $GIT_PASS ]]; then
  echo "GIT_PASS variable not found"
  git_vars=0 
fi

if [[ -z $GIT_AUTHOR_NAME ]]; then
  echo "GIT_AUTHOR_NAME variable not found"
  git_vars=0 
fi

if [[ -z $GIT_COMMITTER_NAME ]]; then
  echo "GIT_COMMITTER_NAME variable not found"
  git_vars=0 
fi

if [[ -z $GIT_AUTHOR_EMAIL ]]; then
  echo "GIT_AUTHOR_EMAIL variable not found"
  git_vars=0 
fi

if [[ -z $GIT_COMMITTER_EMAIL ]]; then
  echo "GIT_COMMITER_EMAIL variable not found"
  git_vars=0 
fi

if [[ $git_vars == 0 ]]; then
  echo 
  echo "WARNING:"
  echo "One or more git variables were not set."
  echo "You will not be able to push/pull to github from inside theia."
  echo
  echo "TIP:"
  echo "you can set these variables in .bashrc or .bash_profile, e.g."
  echo -------------------------------------
  echo export GIT_USER=your_git_username
  echo export GIT_PASS=your_git_password
  echo export GIT_AUTHOR_NAME="Your name"
  echo export GIT_COMMITTER_NAME="Your name"
  echo export GIT_AUTHOR_EMAIL=your@email
  echo export GIT_COMMITTER_EMAIL=your@email
  echo -------------------------------------
  echo

  while true; do
      read -p "Do you want to continue without git configured in Theia?" yn
      case $yn in
          [Yy]* ) break;;
          [Nn]* ) exit;;
          * ) echo "Please answer yes or no.";;
      esac
  done
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  UID_GID_OPTION="-u $(id -u ${USER}):$(id -g ${USER})" 
fi

docker run -it --init \
   -p 3000:3000 \
   ${UID_GID_OPTION} \
   -v "$(pwd):/home/project:cached" \
   -e GIT_USER="$GIT_USER" \
   -e GIT_PASS="$GIT_PASS" \
   -e GIT_AUTHOR_NAME="$GIT_AUTHOR_NAME" \
   -e GIT_COMMITTER_NAME="$GIT_COMMITTER_NAME" \
   -e GIT_AUTHOR_EMAIL="$GIT_AUTHOR_EMAIL" \
   -e GIT_COMMITTER_EMAIL="$GIT_COMMITTER_EMAIL" \
   -e GIT_ASKPASS=/home/project/git_env_password.sh \
   $IMG
