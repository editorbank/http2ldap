#!/bin/env bash
set -e;source $(dirname $0)/config.sh

$docker tag $docker_image $docker_image:$version
$docker login docker.io
$docker push $docker_image:$version
$docker push $docker_image:latest
