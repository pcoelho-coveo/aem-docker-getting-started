FROM python:3.9.10-slim-bullseye

ARG java_version

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main'

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  \
    $java_version \
    wget \
    gcc \
    libcurl4-openssl-dev \
    libssl-dev
        
RUN apt-get clean

# Needed for the pycurl compilation
ENV PYCURL_SSL_LIBRARY=openssl
ENV PYTHONUNBUFFERED 1

RUN /usr/local/bin/python3 -m pip install --no-cache-dir --upgrade \
    pip \
    psutil \
    pycurl \
    urllib3 

ENV TZ=America/Montreal

# Download oak jar
RUN wget https://repository.apache.org/service/local/repositories/releases/content/org/apache/jackrabbit/oak-run/1.8.9/oak-run-1.8.9.jar

# Copy required build media
COPY ./AEM_6.*_Quickstart.jar /opt/aem/AEM_6.x_Quickstart.jar
COPY ./license.properties /opt/aem/license.properties
COPY ./oak-run-*.jar /opt/aem/oak-run.jar

# Extract AEM
WORKDIR /opt/aem
RUN java -Djava.awt.headless=true -Xms8g -Xmx8g -jar AEM_6.x_Quickstart.jar -unpack

# Install utility for AEM
COPY ./base/aem_installer.py /opt/aem/aem_installer.py
COPY ./base/helpers.py /opt/aem/helpers.py