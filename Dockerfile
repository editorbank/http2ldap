FROM ubuntu
ARG main_bin
COPY ./$main_bin /
#CMD /$main_bin
