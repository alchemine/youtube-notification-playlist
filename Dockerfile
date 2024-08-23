# Use the Python base image
ARG VARIANT="3.11-bullseye"
FROM mcr.microsoft.com/devcontainers/python:0-${VARIANT}

# Define the version of Poetry to install
ARG POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=true

# Set the timezone to Asia/Seoul
ENV TZ Asia/Seoul
RUN sudo ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# Set project directory
WORKDIR /app
ENV PYTHONPATH=/app

# Create a Python virtual environment for Poetry and install it
RUN pipx install poetry==${POETRY_VERSION}

# Setup for bash
RUN poetry completions bash >> /home/vscode/.bash_completion && \
    echo "export PATH=.:$PATH" >> ~/.bashrc

# Install Google Chrome
# https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/
RUN sudo apt update && \
    wget -q https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_128.0.6613.84-1_amd64.deb && \
    sudo apt install -yqq ./google-chrome-stable_128.0.6613.84-1_amd64.deb && \
    rm google-chrome-stable_128.0.6613.84-1_amd64.deb && \
    sudo rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install

# Copy the project files
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Open Streamlit server
ENTRYPOINT [ "poetry", "run", "streamlit", "run", "youtube_notification_playlist/app.py" ]