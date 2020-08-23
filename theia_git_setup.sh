#!/bin/bash

git config credential.https://github.com.username $GIT_USER

git_url=$(git config --get remote.origin.url)

USER=$(echo $git_url | sed 's/.*://' | sed 's/\/.*//')
REPO=$(echo $git_url | sed 's/.*://' | sed 's/.*\///')

if [[ git_url != "https://"** ]];
then
    echo "You must use the 'https://github.com/...' git url and not 'git@github.com:..'"
    echo "you can set this with:"

    echo "git remote set-url origin https://github.com/$USER/$REPO"
    exit 1
fi