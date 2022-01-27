# AEM & Docker getting started guide

## Prerequisites

- [Docker](https://www.docker.com) with at least 8GB memory allocated.
- AEM installation file, named `AEM_6.4_Quickstart.jar` or `AEM_6.5_Quickstart.jar`
- AEM license file, named `license.properties`

## Getting started: running AEM

1. Clone this repo
2. Copy the `license.properties` and AEM `AEM_6.x_Quickstart.jar` to the root path.
3. Place AEM packages `./author/packages/` and/or `./publisher/packages/` (they will be installed at build time).
4. Build images for `AEM 6.4` 
* `docker build -t aem-base --build-arg java_version=openjdk-8-jre -f base/Dockerfile . && docker-compose build --progress=plain`
5. Build images for `AEM 6.5`
* `docker build -t aem-base --build-arg java_version=openjdk-11-jre -f base/Dockerfile . && docker-compose build --progress=plain`
6. Start containers `docker-compose up`. 
7. A volume will be mounted on `./logs` on your local system to the containers, so you have easy access to the logs of all containers.
8. Wait until AEM has fully started. To check for the author, open the [bundles page](http://localhost:4502/system/console/bundles) and when all bundle statuses are either `Active` or `Fragment` the AEM environment has fully started.
9. Navigate to [http://localhost:4502](http://localhost:4502) and you'll see a login screen. Login with username `admin` and password `admin`.
10. Navigate to [http://localhost:4503](http://localhost:4503) and you will see the assets on the publish instance.
11. Navigate to [http://localhost:8080](http://localhost:8080) to see the published site via the dispatcher. 

## Some infos

- Using `docker-compose stop` or `ctrl + c` the containers state is preserved.
- Running `docker-compose down` will delete persisted data of the containers.
- Images need to be rebuild when changing packages in the `packages` directories.
- `aem-coveo-connector` can be installed/uninstalled by using maven task configured on the project.
- Document links will be pointing to `http://publisher:4503` because the publish address on the externalizer is set to `http://publisher:4503`. The author 
container is not able to make http requests using `http://localhost:4503` because it's running on a separate container. However, the `hostname` of the publisher container is not available
on the host machine but we forward `4503:4503` port from the publisher container to the host port. So the document link can be accessed on `http://localhost:4503/my-document/etc/doc.html`.
You can also edit the `C:\Windows\System32\drivers\etc\hosts` file by adding `127.0.0.1 publisher` so it will properly the urls (we may automate that step later). 
   
# Credits

Inspiration and code examples are taken from the following projects:

- [Original Repo from where this fork is based](https://github.com/remcorakers/aem-docker-getting-started)
- [https://github.com/AdobeAtAdobe/aem_6-1_docker](https://github.com/AdobeAtAdobe/aem_6-1_docker)
- [https://hub.docker.com/r/ggotti/aem-base](https://hub.docker.com/r/ggotti/aem-base)
- [https://github.com/adfinis-sygroup/aem-docker](https://github.com/adfinis-sygroup/aem-docker)