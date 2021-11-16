# AEM & Docker getting started guide

## Prerequisites

- [Docker](https://www.docker.com) with at least 8GB memory allocated.
- AEM installation file, named `AEM_6.4_Quickstart.jar` or `AEM_6.5_Quickstart.jar`
- AEM license file, named `license.properties`

## Getting started: running AEM

1. Clone this repo
2. Copy the license and AEM `quick start` jar on the root path.
3. AEM packages can be placed on `./author/packages/` and `./publisher/packages/` and they will be installed at build time.
4. `AEM 6.4` => Build the Docker images with `docker build -t aem-base --build-arg java_version=java-1.8.0-openjdk -f base/Dockerfile . && docker-compose build`.
5. `AEM 6.5` => Build the Docker images with `docker build -t aem-base --build-arg java_version=java-11-openjdk -f base/Dockerfile . && docker-compose build`.
6. Start the containers with `docker-compose up`. 
7. A volume will be mounted on `./logs` on your local system to the containers, so you have easy access to the logs of all containers.
8. Wait until AEM has fully started. To check for the author, open the [bundles page](http://localhost:4502/system/console/bundles) and when all bundle statusses are either `Active` or `Fragment` the AEM environment has fully started.
9. Navigate to [http://localhost:4502](http://localhost:4502) and you'll see a login screen. Login with username `admin` and password `admin`.
10. Navigate to [http://localhost:4503](http://localhost:4503) and you will see the assets on the publish instance.
11. Navigate to [http://localhost:8080](http://localhost:8080) to see the published site via the dispatcher. 

## Some infos

 - Starting (`docker-compose up`) and stopping (`docker-compose stop`) the containers preserves AEM content.
 - Images need to be rebuild when changing packages in the `packages` directories.
 - Running `docker-compose down` will delete persisted data of the containers.
 - We can still install and uninstall the coveo connector from the maven task we have configured

## Credits

Inspiration and code examples are taken from the following projects:

- [Original Repo from where this fork is based](https://github.com/remcorakers/aem-docker-getting-started)
- [https://github.com/AdobeAtAdobe/aem_6-1_docker](https://github.com/AdobeAtAdobe/aem_6-1_docker)
- [https://hub.docker.com/r/ggotti/aem-base](https://hub.docker.com/r/ggotti/aem-base)
- [https://github.com/adfinis-sygroup/aem-docker](https://github.com/adfinis-sygroup/aem-docker)
