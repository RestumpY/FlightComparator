import scrapy


class OpodoSpider(scrapy.Spider):
    name = "opodo"
    allowed_domains = ["www.opodo.fr"]
    start_urls = ["https://www.opodo.fr/"]

    def parse(self, response):
        pass
