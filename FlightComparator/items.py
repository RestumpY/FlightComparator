# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightcomparatorItem(scrapy.Item):
    dateAller = scrapy.Field()
    dateRetour = scrapy.Field()
    destinationAller = scrapy.Field()
    destinationRetour = scrapy.Field()
    nbrPlaces = scrapy.Field()
    compagnie = scrapy.Field()
    prix = scrapy.Field()
    pass
