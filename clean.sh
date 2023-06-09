#!/bin/env bash
set -e;source $(dirname $0)/config.sh

# Удаление контейнеров и образов сделанных проектом
$docker ps -q -a -f name=$docker_container | xargs -r $docker rm -f
$docker images -q -f reference=$docker_image | xargs -r $docker rmi -f

# Удаление игнорируемых Git-ом файлов кроме *.bak (как файлов так и директорий)
git ls-files --others --ignored --exclude-standard | grep -v .bak | xargs -r -i rm {}

# Удаление только пустых директорий
find . -empty -type d -delete
