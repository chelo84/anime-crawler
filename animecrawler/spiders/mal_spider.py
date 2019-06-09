import scrapy
from animecrawler.parser.mal_item_parser import MALItemParser
from animecrawler.utils.extract_utils import ExtractUtils


class MALSpider(scrapy.Spider):
    name = 'mal_1'
    anime_url = '{hostname}{path}'.format(hostname=ExtractUtils.MAL_URL, path='/anime.php?letter=')
    letters = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z']
    ANIMES_PER_PAGE = 50

    def start_requests(self):
        for letter in self.letters:
            yield scrapy.Request(url='{url}{letter}'.format(url=self.anime_url, letter=letter), callback=self.parse)

    def parse(self, response):
        urls = response.xpath(
            '//div[contains(@class, "js-categories-seasonal") or contains(@class, "list")]/table/tr[position()>1]/td[2]//a[contains(@class, "hovertitle") or contains(@class, "hoverinfo_trigger")]//@href').getall()

        for url in urls:
            yield scrapy.Request(url=url, callback=MALItemParser.parse_anime)

        next_page_path = response.xpath('//*[@id="content"]/div[5]/div/div/span[normalize-space(text()[1])!=""]/text()[1]/following-sibling::a/@href').get()
        if next_page_path:
            next_page = '{hostname}{path}'.format(hostname=ExtractUtils.MAL_URL, path=next_page_path)
            yield scrapy.Request(url=next_page, callback=self.parse)
