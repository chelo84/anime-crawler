# Anime crawler

Anime crawler developed with Python and Scrapy.

Used the website www.anime-planet.com for scrapping.

##Pre-requisites
* Python
* MongoDB
    * **Server**: localhost
    * **Port**: 27017
* pycurl
* Run the command `py setup.py install` inside the root folder to install the requirements after having Python and pyCurl installed


##How to run
* Run the command `scrapyd` to start the server and then `scrapyd-deploy -p animecrawler` to deploy the project
* Run the file named `start-spiders.sh` through the command line and check `http://localhost:6800/jobs` to see the situation of the running jobs