# projectR
for R

# Construction

Although this can be run as a standalone app, for the purposes of this project the app is designed to run within a local network of containers each hosting a separate micro service.

* API - api/src/api.py contains the code for the REST API. This is deployed three times within 3 distinct containers listening on host ports 5001, 5002, 5003.

* Database - a MySQL database is deployed and configured listening on host port 3307

* Load Balancer - to demonstate the intended distribution of the API instances, I have configured an NginX load balancer to listen on the defaul Flask port of 5000 and round robin the requests to the 3 API urls.


# How to run
This application can be deployed as a standalone python/flaskRESTful app or within containers

To run as a standalone app 
python api/src/api.py
This will require you to have a MySQL database configured with the appropriate tables and available to the app with credentials defined in settings.yaml

Recommended deployment is within the docker setup defined in docker-compose.yaml

To build and launch this on a linux system, execute the following two commands
* docker-compose build
* docker-compose up



# Cloud Deployment
1. Make use of Google hosted database with built in replication