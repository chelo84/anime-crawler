from scrapy.crawler import CrawlerProcess
from animecrawler.spiders.anime_spider import AnimesSpider1
from animecrawler.spiders.anime_spider_2 import AnimesSpider2
from animecrawler.spiders.anime_spider_3 import AnimesSpider3
from animecrawler.spiders.anime_spider_4 import AnimesSpider4
from animecrawler.spiders.anime_spider_5 import AnimesSpider5
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(AnimesSpider1)
process.crawl(AnimesSpider2)
process.crawl(AnimesSpider3)
process.crawl(AnimesSpider4)
process.crawl(AnimesSpider5)
process.start()