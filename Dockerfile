# syntax=docker/dockerfile:1
#FROM alchemine/base-cuda:11.8.0-cudnn8-runtime-ubuntu22.04
FROM selenium/standalone-chrome:119.0

#SHELL ["/bin/bash", "-ic"]
#
## generate environment in project directory
#ENV POETRY_VIRTUALENVS_IN_PROJECT=true
#WORKDIR /opt/project
#
## copy poetry configurations
#COPY pyproject.toml /opt/project/
##COPY poetry.lock pyproject.toml /opt/project/
#
## install python environment
#RUN poetry env use python3.10 && \
#    poetry install --no-root
#
## copy all files
#COPY . /opt/project
