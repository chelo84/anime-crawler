# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'animecrawler',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = animecrawler.settings']},
    install_requires=['scrapy==1.6', 'pymongo==3.8', 'scrapyd==1.2.0', 'scrapyd-client==1.2.0a1', 'Twisted==22.4.0']
)
