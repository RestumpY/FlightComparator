import scrapy


class MomondoSpider(scrapy.Spider):
    name = "momondo"
    allowed_domains = ["www.momondo.fr"]
    start_urls = ["https://www.momondo.fr/"]

    def parse(self, response):
        pass
