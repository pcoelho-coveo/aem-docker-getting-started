FROM websites-aem-base

WORKDIR /opt/aem

COPY ./author/packages/* /opt/aem/packages/

RUN python3 aem_installer.py -i AEM_6.x_Quickstart.jar -r author,local -p 4502

EXPOSE 4502
CMD java -Xms4g -Xmx4g -Djava.awt.headless=true -Xdebug -Xnoagent -agentlib:jdwp=transport=dt_socket,address=5005,server=y,suspend=n -jar AEM_6.x_Quickstart.jar -p 4502 -r author,local -v -nofork
