import scrapy


class KayakSpider(scrapy.Spider):
    name = "kayak"
    allowed_domains = ["www.kayak.fr"]
    start_urls = ["https://www.kayak.fr/"]

    def parse(self, response):
        pass
