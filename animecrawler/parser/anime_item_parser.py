from animecrawler.utils.extract_utils import ExtractUtils
from animecrawler.items import AnimeItem
from scrapy.http import HtmlResponse
import scrapy


class AnimeItemParser:

    CHARACTER_TYPES = {
        'MAIN': 1,
        'SECONDARY': 2,
        'MINOR': 3
    }

    @staticmethod
    def parse_anime(response):
        anime_item = AnimeItem()
        anime_item['url'] = response.request.url
        anime_item['name'] = ExtractUtils.extract_default_blank(response, 'h1[itemprop="name"]::text')
        anime_item['aka'] = ExtractUtils.extract_default_blank(response, 'h2.aka::text')
        anime_item['description'] = ExtractUtils.extract_default_blank(response, 'div[itemprop="description"] p::text')
        anime_item['type'] = ExtractUtils.extract_x_path_default_blank(response, '//*[@id="siteContainer"]/section[1]/div[1]/span//text()')
        anime_item['studio'] = ExtractUtils.extract_x_path_default_blank(response, '//*[@id="siteContainer"]/section[1]/div[2]/a//text()')
        anime_item['rating'] = "{:.2f}".format(float(ExtractUtils.extract_x_path(response, '//*[@id="siteContainer"]/section[1]/div[4]/div/meta[1]/@content').get(default=0.0)))
        anime_item['rating_count'] = ExtractUtils.extract_x_path(response, '//*[@id="siteContainer"]/section[1]/div[4]/div/meta[4]/@content').get(default=0)
        anime_item['tags'] = list(map(lambda tag: tag.strip(), ExtractUtils.extract_x_path(response, '//li[@itemprop="genre"]//a/text()').getall()))
        anime_item['date'] = ExtractUtils.extract_x_path_default_blank(response, '//*[@id="siteContainer"]/section[1]/div[3]/span/text()')
        anime_item['image'] = '{hostname}{path}'.format(hostname=ExtractUtils.ANIME_PLANET_URL,
                                                        path=ExtractUtils.extract_x_path_default_blank(response, '//*[@id="entry"]/div[1]/div[1]/div[1]/div/img/@src'))

        yield scrapy.Request(url=response.request.url + '/characters', callback=AnimeItemParser.__parse_characters,
                             meta=anime_item)

    @staticmethod
    def __parse_characters(response):
        anime_item = response.meta

        characters = {
            'main': AnimeItemParser.__parse_characters_by_type(response, AnimeItemParser.CHARACTER_TYPES['MAIN']),
            'secondary': AnimeItemParser.__parse_characters_by_type(response, AnimeItemParser.CHARACTER_TYPES['SECONDARY']),
            'minor': AnimeItemParser.__parse_characters_by_type(response, AnimeItemParser.CHARACTER_TYPES['MINOR'])
        }

        anime_item['characters'] = characters

        yield anime_item

    @staticmethod
    def __parse_characters_by_type(response, character_type):
        table = ExtractUtils.extract_x_path(response, '//*[@id="siteContainer"]/section/div[2]/table[{character_type}]//tr'.format(character_type=character_type)).getall()
        characters = AnimeItemParser.__get_characters_from_table(response, table)

        return characters

    @staticmethod
    def __get_characters_from_table(response, table):
        characters = []
        for tr in table:
            character = {}
            tr_response = HtmlResponse(response.url,
                                       encoding='utf-8',
                                       body=tr)
            character['avatar'] = '{hostname}{path}'.format(hostname=ExtractUtils.ANIME_PLANET_URL,
                                                            path=ExtractUtils.extract_x_path_default_blank(tr_response, '//td[1]/a/@href'))
            character['url'] = '{hostname}{path}'.format(hostname=ExtractUtils.ANIME_PLANET_URL,
                                                         path=ExtractUtils.extract_x_path_default_blank(tr_response,  '//td[2]/a/@href'))
            character['name'] = ExtractUtils.extract_x_path_default_blank(tr_response, '//td[2]/a/text()')
            character['tags'] = list(map(lambda tag: tag.strip(), ExtractUtils.extract_x_path(tr_response,  '//td[2]/div/ul/li/a/text()').getall()))
            character['actors'] = AnimeItemParser.__parse_characters_actors(tr_response)

            characters.append(character)

        return characters

    @staticmethod
    def __parse_characters_actors(response):
        actors_lang = list(map(lambda lang: lang.strip().replace('.', ''), ExtractUtils.extract_x_path(response, '//td[4]/div/text()').getall()))
        actors_names = list(ExtractUtils.extract_x_path(response, '//td[4]/div/a/text()').getall())
        actors = []
        non_speaking_role = 'Non-Speaking Role'
        for i in range(0, len(actors_lang)):
            actor = {
                'language': non_speaking_role if actors_lang[i] == non_speaking_role else actors_lang[i],
                'name': '' if actors_lang[i] == non_speaking_role else actors_names[i]
            }
            actors.append(actor)

        return actors
