from animecrawler.utils.extract_utils import ExtractUtils
from animecrawler.items import MALItem
from scrapy.http import HtmlResponse
from datetime import datetime
import scrapy


class MALItemParser:

    @staticmethod
    def parse_anime(response):
        item = MALItem()
        item['url'] = response.request.url
        item['name'] = ExtractUtils.extract_x_path_default_blank(response, '//*[@id="contentWrapper"]/div[1]/h1/span')
        item['japanese_name'] = ExtractUtils.extract_x_path_default_blank(response, '//div[@class="spaceit_pad"]/span[@class="dark_text" and text()="Japanese:"]/../text()')
        item['type'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Type:"]/../a/text()')
        item['episodes'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Episodes:"]/../text()')
        item['status'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Status:"]/../text()')

        aired = MALItemParser.__parse_aired(response)
        item['aired_from'] = aired['from']
        item['aired_to'] = aired['to']
        item['premiered'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Premiered:"]/../a/text()')
        item['broadcast'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Broadcast:"]/../text()')
        item['producers'] = response.xpath('//div/span[@class="dark_text" and text()="Producers:"]/../a/text()').getall()
        item['licensors'] = response.xpath('//div/span[@class="dark_text" and text()="Licensors:"]/../a/text()').getall()
        item['studios'] = response.xpath( '//div/span[@class="dark_text" and text()="Studios:"]/../a/text()').getall()
        item['source'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Source:"]/../text()')
        item['genres'] = response.xpath('//div/span[@class="dark_text" and text()="Genres:"]/../a/text()').getall()
        item['duration'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Duration:"]/../a/text()')
        item['rating'] = float(response.xpath('//div/span[@class="dark_text" and text()="Rating:"]/../a/text()').get(default='0.00').strip())
        item['score'] = ExtractUtils.extract_x_path_default_blank(response, '//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]/div[@data-title="score"]/text()')
        item['scored_by'] = ExtractUtils.extract_x_path_default_blank(response, '//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]/div[@data-title="score"]/@data-user')
        item['ranked'] = int(response
                             .xpath('//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]//span[contains(@class, "ranked")]/strong/text()').get(default='0').replace('#', ''))
        item['popularity'] = int(response
                                 .xpath('//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]//span[contains(@class, "popularity")]/strong/text()').get(default='0').replace('#', ''))
        item['members'] = int(response
                              .xpath( '//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]//span[contains(@class, "members")]/strong/text()').get(default='0').replace(',', ''))
        item['synopsis'] = response.xpath('//span[@itemprop="description"]//text()').getall()

    @staticmethod
    def __parse_aired(response):
        aired = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Aired:"]/../text()').split('to')

        aired_from = '' if len(aired) < 1 or aired[0].strip() == '' \
            else datetime.strptime(aired[0].strip(), '%b %d, %Y')
        aired_to = '' if len(aired) < 2 or aired[1].strip() == '' \
            else datetime.strptime(aired[1].strip(), '%b %d, %Y')

        return {
            'from': aired_from,
            'to': aired_to
        }
