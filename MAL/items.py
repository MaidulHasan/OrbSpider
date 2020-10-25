# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
"""
to know more about the scrapy processors visit -
https://itemloaders.readthedocs.io/en/latest/built-in-processors.html#built-in-processors
"""
import scrapy
from scrapy.loader.processors import TakeFirst


class MalItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()  # anime thumbnails
    anime_title = scrapy.Field(
        output_processors=TakeFirst()
    )
    personal_rating = scrapy.Field()
