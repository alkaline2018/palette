# Dockerfile
# without an file extension

# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app
RUN apt-get update && apt-get install -y && apt-get install -y vim
# copy the dependencies file to the working directory
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host ftp.daumkakao.com -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

