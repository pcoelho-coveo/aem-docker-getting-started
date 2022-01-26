FROM httpd:alpine3.15

RUN apk update && apk upgrade
RUN apk --no-cache add \
    tar \
    wget \
    --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
    && \
    rm -rf /var/cache/apk/*

ENV TZ=America/Montreal

# Download the dispatcher
RUN wget https://download.macromedia.com/dispatcher/download/dispatcher-apache2.4-linux-x86_64-ssl1.0-4.3.3.tar.gz
RUN tar -zxvf dispatcher-apache2.*.tar.gz

# Copy the dispatcher
RUN cp ./dispatcher-apache2.*.so /usr/local/apache2/modules
RUN ln -s /usr/local/apache2/modules/dispatcher-apache2.*.so /usr/local/apache2/modules/mod_dispatcher.so

# Add config files
ADD ./httpd.conf /usr/local/apache2/conf/httpd.conf
ADD ./aem-disp2.conf /usr/local/apache2/conf.d/aem-disp2.conf
ADD ./proxy.conf /usr/local/apache2/conf.d/zzz-proxy.conf
ADD ./dispatcher.any /usr/local/apache2/conf/dispatcher.any

RUN ls /usr/local/apache2/

## Set permissions
#RUN chown -R daemon:daemon /var/www/html
#
#EXPOSE 80 443
#CMD /usr/sbin/httpd -D FOREGROUND