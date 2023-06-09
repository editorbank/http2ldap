### config ###
export main=http2ldap
export version=1.0.$(date +%y%m%d)
export docker=podman
export docker_image=docker.io/editorbank/$main
export docker_container=$main
export dockerfile_dir=.

cd $(dirname $0)
