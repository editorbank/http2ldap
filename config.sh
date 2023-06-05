### config ###
export main=http2ldap
export docker=podman
export docker_image=docker.io/editorbank/$main:latest
export docker_container=$main
export dockerfile_dir=.

cd $(dirname $0)
