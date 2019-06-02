import scrapy

class AnimesSpider1(scrapy.Spider):
    name = 'animes'
    anime_planet_url = 'https://www.anime-planet.com/anime/all'
    startAt = 1

    def start_requests(self):
        yield scrapy.Request(url=self.anime_planet_url, callback=self.get_urls)

    def get_urls(self, response):
        pages = (max(list(map(lambda str: int(str.replace("?page=", '')),
                              response.css('div.pagination.aligncenter li a::attr(href)').getall()))))
        urls = []
        for i in range(self.startAt, pages//5):
            urls.append(self.anime_planet_url + '?page=' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('ul.cardDeck.cardGrid a::attr(href)').extract():
            url = 'https://www.anime-planet.com' + href
            yield scrapy.Request(url, self.parse_anime)

    def parse_anime(self, response):
        def extract(query):
            return response.css(query).get(default='').strip()
        def extract_multiple(query):
            return response.xpath(query).getall()

        yield {
            'name': extract('h1[itemprop="name"]::text'),
            'aka': extract('h2.aka::text'),
            'description': extract('div[itemprop="description"] p::text'),
            'tags': list(map(lambda tag: tag.strip(), extract_multiple('//li[@itemprop="genre"]//a//text()')))
        }