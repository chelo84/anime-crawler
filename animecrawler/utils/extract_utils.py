
class ExtractUtils:

    ANIME_PLANET_URL = 'https://www.anime-planet.com'
    MAL_URL = 'https://myanimelist.net'

    @staticmethod
    def extract_default_blank(response, query):
        return response.css(query).get(default='').strip()

    @staticmethod
    def extract(response, query):
        return response.css(query)

    @staticmethod
    def extract_x_path_default_blank(response, query):
        return response.xpath(query).get(default='').strip()

    @staticmethod
    def extract_x_path(response, query):
        return response.xpath(query)

    @staticmethod
    def extract_x_path_with_regex(response, query, regex):
        return response.xpath(query).re(regex)
