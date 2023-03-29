FROM python:3.9

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /e-commerce

# Set the working directory to /music_service
WORKDIR /e_commerce

# Copy the current directory contents into the container at /music_service
ADD . /e_commerce/

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# running migrations