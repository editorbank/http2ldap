#!/bin/env bash
[ -z "$1" -o  "--help" == "$1" ] && echo "Use: $0 <file.py>" && exit 1

docker=podman
docker_image=docker.io/editorbank/py2bin

$docker run -it --rm -v $PWD:/pwd --name py2bin-$RANDOM $docker_image /compile.sh $@
