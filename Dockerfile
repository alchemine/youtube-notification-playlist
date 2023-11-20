# syntax=docker/dockerfile:1
FROM alchemine/base-cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# copy project directory
COPY . /project
WORKDIR /project

# install python environment
RUN poetry env use python3.8 && \
    poetry install --no-root
