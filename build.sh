#!/bin/env bash
set -e;source $(dirname $0)/config.sh

[ ! -f "./$main.bin" -o "./$main.bin" -ot "./$main.py" ] && ./py2bin.sh ./$main.py 

# Удаление контейнеров и образов сделанных проектом
$docker ps -q -a -f name=$docker_container | xargs -r $docker rm -f
$docker images -q -f reference=$docker_image | xargs -r $docker rmi -f

$docker build \
  --tag $docker_image \
  --build-arg main_bin="./$main.bin" \
  $dockerfile_dir

$docker run -it --rm \
  --name $docker_container \
   $docker_image \
   /$main.bin --help
