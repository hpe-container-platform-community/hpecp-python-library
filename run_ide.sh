#!/usr/bin/env bash

IMG=hpecp/hpecp-ide:latest

if [[ "$(docker images -q $IMG 2> /dev/null)" == "" ]]; then
  ./build_ide.sh
fi

docker run -it --init -p 3000:3000 -v "$(pwd):/home/project:cached" -e GIT_USER="$GIT_USER" -e GIT_PASS="$GIT_PASS" -e GIT_AUTHOR_NAME="$GIT_AUTHOR_NAME" -e GIT_COMMITTER_NAME="$GIT_COMMITTER_NAME" -e GIT_AUTHOR_EMAIL="$GIT_AUTHOR_EMAIL" -e GIT_COMMITTER_EMAIL="$GIT_COMMITTER_EMAIL" -e GIT_ASKPASS=/home/project/git_env_password.sh $IMG
