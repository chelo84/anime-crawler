import re
from animecrawler.utils.extract_utils import ExtractUtils
from animecrawler.items import AnimeItem

class AnimeItemParser:

    @staticmethod
    def parse_anime(response):
        anime_item = AnimeItem()
        anime_item['url'] = response.request.url
        anime_item['name'] = ExtractUtils.extract_default_blank(response, 'h1[itemprop="name"]::text')
        anime_item['aka'] = ExtractUtils.extract_default_blank(response, 'h2.aka::text')
        anime_item['description'] = ExtractUtils.extract_default_blank(response, 'div[itemprop="description"] p::text')
        anime_item['type'] = ExtractUtils.extract_x_path_default_blank(response, '//*[@id="siteContainer"]/section[1]/div[1]/span//text()')
        anime_item['studio'] = ExtractUtils.extract_x_path(response, '//*[@id="siteContainer"]/section[1]/div[2]/a//text()').get()
        anime_item['rating'] = "{:.2f}".format(float(ExtractUtils.extract_x_path(response, '//*[@id="siteContainer"]/section[1]/div[4]/div/meta[1]/@content').get(default=0.0)))
        anime_item['rating_count'] = ExtractUtils.extract_x_path(response, '//*[@id="siteContainer"]/section[1]/div[4]/div/meta[4]/@content').get(default=0)
        anime_item['tags'] = list(map(lambda tag: tag.strip(), ExtractUtils.extract_x_path(response, '//li[@itemprop="genre"]//a//text()').getall()))
        anime_item['date'] = ExtractUtils.extract_x_path_default_blank(response, '//*[@id="siteContainer"]/section[1]/div[3]/span/text()')

        yield anime_item
