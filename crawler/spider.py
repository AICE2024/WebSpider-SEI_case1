import scrapy
import os
from pathlib import Path
from ..items import ClimateFinanceItem

class ClimateFinanceSpider(scrapy.Spider):
    name = "climate_finance"
    allowed_domains = ['oecd.org', 'worldbank.org']
    start_urls = [
        'https://www.oecd.org/',
        'https://www.worldbank.org/'
    ]

    def parse(self, response):
        titles = response.css('h1::text, h2::text').getall()
        paragraphs = response.css('p::text').getall()

        if titles or paragraphs:
            item = ClimateFinanceItem()
            item['url'] = response.url
            item['titles'] = titles
            item['content'] = paragraphs
            yield item

        for next_page in response.css('a::attr(href)').getall():
            if next_page and next_page.startswith('/'):
                yield response.follow(next_page, callback=self.parse)
