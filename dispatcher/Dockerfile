FROM httpd:2.4.52-bullseye

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget

RUN apt-get clean

ENV TZ=America/Montreal

# Download the dispatcher
RUN wget -qO- https://download.macromedia.com/dispatcher/download/dispatcher-apache2.4-linux-x86_64-ssl1.1-4.3.4.tar.gz | tar -zxvf -

# Copy the dispatcher
RUN cp ./dispatcher-apache2.*.so /usr/local/apache2/modules
RUN ln -s /usr/local/apache2/modules/dispatcher-apache2.*.so /usr/local/apache2/modules/mod_dispatcher.so

# Add config files
ADD ./httpd.conf /usr/local/apache2/conf/httpd.conf
ADD ./httpd-dispatcher.conf /usr/local/apache2/conf/extra/httpd-dispatcher.conf
ADD ./proxy.conf /usr/local/apache2/conf/extra/zzz-proxy.conf
ADD ./dispatcher.any /usr/local/apache2/conf/dispatcher.any

# Remove index html
RUN rm /usr/local/apache2/htdocs/index.html

## Set permissions
RUN chown -R daemon:daemon /usr/local/apache2/htdocs

EXPOSE 80 443