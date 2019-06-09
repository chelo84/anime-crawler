from animecrawler.utils.extract_utils import ExtractUtils
from animecrawler.items import MALItem
from functools import reduce


class MALItemParser:

    @staticmethod
    def parse_anime(response):
        item = MALItem()
        item['url'] = response.request.url
        item['name'] = ExtractUtils.extract_x_path_default_blank(response, '//*[@id="contentWrapper"]/div[1]/h1/span/text()')
        item['type'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Type:"]/../a/text()')
        item['episodes'] = MALItemParser.__reduce_str(response.xpath('//div/span[@class="dark_text" and text()="Episodes:"]/../text()').getall())
        item['status'] = MALItemParser.__reduce_str(response.xpath('//div/span[@class="dark_text" and text()="Status:"]/../text()').getall())

        aired = MALItemParser.__parse_aired(response)
        item['aired_from'] = aired['from']
        item['aired_to'] = aired['to']
        item['premiered'] = ExtractUtils.extract_x_path_default_blank(response, '//div/span[@class="dark_text" and text()="Premiered:"]/../a/text()')
        item['broadcast'] = MALItemParser.__reduce_str(response.xpath('//div/span[@class="dark_text" and text()="Broadcast:"]/../text()').getall())
        item['producers'] = response.xpath('//div/span[@class="dark_text" and text()="Producers:"]/../a[text()!="add some"]/text()').getall()
        item['licensors'] = response.xpath('//div/span[@class="dark_text" and text()="Licensors:"]/../a[text()!="add some"]/text()').getall()
        item['studios'] = response.xpath( '//div/span[@class="dark_text" and text()="Studios:"]/../a[text()!="add some"]/text()').getall()
        item['source'] = MALItemParser.__reduce_str(response.xpath('//div/span[@class="dark_text" and text()="Source:"]/../text()').getall())
        item['genres'] = response.xpath('//div/span[@class="dark_text" and text()="Genres:"]/../a/text()').getall()
        item['duration'] = MALItemParser.__reduce_str(response.xpath('//div/span[@class="dark_text" and text()="Duration:"]/../a/text()').getall())
        item['rating'] = MALItemParser.__reduce_str(response.xpath('//div/span[@class="dark_text" and text()="Rating:"]/../a/text()').getall())
        item['score'] = ExtractUtils.extract_x_path_default_blank(response, '//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]/div[@data-title="score"]/text()')
        item['scored_by'] = ExtractUtils.extract_x_path_default_blank(response, '//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]/div[@data-title="score"]/@data-user')
        item['ranked'] = response.xpath('//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]//span[contains(@class, "ranked")]/strong/text()').get(default='N/A').replace('#', '')
        item['popularity'] = int(response
                                 .xpath('//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]//span[contains(@class, "popularity")]/strong/text()').get(default='0').replace('#', ''))
        item['members'] = int(response
                              .xpath( '//div[contains(@class, "anime-detail-header-stats")]/div[contains(@class, "stats-block")]//span[contains(@class, "members")]/strong/text()').get(default='0').replace(',', ''))
        item['synopsis'] = MALItemParser.__reduce_str(response.xpath('//span[@itemprop="description"]//text()').getall())

        yield item

    @staticmethod
    def __reduce_str(str_list):
        return reduce(lambda x1, x2: '{x1}{x2}'.format(x1=(x1 or '').strip(), x2=(x2 or '').strip()),
                      str_list,
                      '')

    @staticmethod
    def __parse_aired(response):
        aired = MALItemParser.__reduce_str(response.xpath('//div/span[@class="dark_text" and text()="Aired:"]/../text()').getall()).split('to')

        aired_from = '' if len(aired) < 1 or aired[0].strip() == '' \
            else aired[0].strip()
        aired_to = '' if len(aired) < 2 or aired[1].strip() == '' \
            else aired[1].strip()

        return {
            'from': aired_from,
            'to': aired_to
        }
