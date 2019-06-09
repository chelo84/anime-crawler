# Anime crawler

Anime crawler developed with Python and Scrapy using Scrapyd as the spider's orchestrator.


## Pre-requisites
* Python
* MongoDB
    * **Server**: localhost
    * **Port**: 27017
* pycurl
* It is strictly needed Twisted version 18.9.0
* Run the command `py setup.py install` inside the root folder to install the requirements after having Python and pyCurl installed


## How to run
* Run the command `scrapyd` to start the server and then `scrapyd-deploy -p animecrawler` to create the eggs and deploy the project
* Run the file named `start-anime-planet-spiders.sh` or `start-myanimelist-spiders.sh` through the command line 
* Check `http://localhost:6800/jobs` to see the situation of the running jobs