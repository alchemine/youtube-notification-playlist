# syntax=docker/dockerfile:1
FROM alchemine/base-cuda:11.8.0-cudnn8-runtime-ubuntu22.04
LABEL maintainer="alchemine <djyoon0223@gmail.com>"

SHELL ["/bin/bash", "-ic"]

# install google-chrome-stable (version: 119)
RUN apt update

RUN wget -q http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_119.0.6045.159-1_amd64.deb && \
    apt install -yqq ./google-chrome-stable_119.0.6045.159-1_amd64.deb && \
    rm google-chrome-stable_119.0.6045.159-1_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# generate environment in project directory
WORKDIR /opt/project

## copy poetry configurations
#COPY poetry.lock pyproject.toml /opt/project/
#
## install python environment
#RUN poetry env use python3.10 && \
#    poetry install --no-root
#
## copy all files
#COPY . /opt/project
