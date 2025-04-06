"""
This code is a web scraper (spider) that collects information from certain websites, 
such as the OECD, World Bank, and Google Scholar. It works as follows:
 1. The spider starts by visiting a list of specified URLs (websites).
 2. It looks for the title and content of the web pages. If it can't find content in one place, 
    it checks other areas of the page.
 3. It saves the data (the URL, title, and content) in a structured format called JSON Lines.
 4. The spider then looks for links to other pages on the site that might contain articles. 
    If it finds these links, it follows them and continues scraping.
 5. The settings are configured to prevent being blocked by the websites. This includes:
    - Pretending to be a regular browser to avoid detection
    - Delaying requests between pages to avoid sending too many requests in a short time
    - Ignoring robots.txt files that might prevent scraping
"""

import scrapy
import json
from pathlib import Path

                                                                            # Define the item to store the scraped data
class ClimateFinanceItem(scrapy.Item):
    url = scrapy.Field()                                                    # Store the URL of the page
    titles = scrapy.Field()                                                 # Store the title of the page
    content = scrapy.Field()                                                # Store the main content of the page

                                                                            # Define the spider to scrape the websites
class ClimateFinanceSpider(scrapy.Spider):
    name = "climate_finance"                                                # Name of the spider
    allowed_domains = ['oecd.org', 'worldbank.org', 'scholar.google.com']   # Only scrape these websites
    start_urls = [
        'https://www.oecd.org/',                                            # Start scraping from these URLs
        'https://www.worldbank.org/ext/en/home',
        'https://scholar.google.com/'
    ]

                                                                            # Settings for the spider
    custom_settings = {
        'DEPTH_LIMIT': None,                                                # No limit on how deep the spider can go (crawl multiple levels)
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',  # Pretend to be a regular browser to avoid being blocked
        'FEED_FORMAT': 'jsonlines',                                         # Save the data in jsonlines format
        'FEED_URI': 'data/raw/scraped_data.jsonl',                          # Path where the data will be saved
        'FEED_EXPORT_ENCODING': 'utf-8',                                    # Save the file in UTF-8 encoding
        'ROBOTSTXT_OBEY': False,                                            # Ignore the robots.txt file (don't follow any rules in it)
        'DOWNLOAD_DELAY': 1,                                                # Wait 1 second between requests to avoid being blocked
    }

                                                                            # Function to process the content of each page
    def parse(self, response):
        title = response.xpath('//title/text()').get()                      # Get the title of the page

                                                                            # Try to get content from the page using a specific CSS class
        content = response.xpath('//div[contains(@class, "content")]/text()').getall()
        if not content:                                                     # If no content is found, get text from paragraph tags
            content = response.css('p::text').getall()
        
                                                                            # Print out the URL, title, and content for debugging
        print(f"Scraping URL: {response.url}")
        print(f"Title: {title}")
        print(f"Content: {content}")

                                                                            # Create an item with the scraped data
        item = ClimateFinanceItem(
            url=response.url,                                               # Store the URL of the page
            titles=[title],                                                 # Store the title of the page
            content=content                                                 # Store the content from the page
        )

                                                                            # Yield the item (send it for saving or further processing)
        yield item

                                                                            # Find all links on the page and follow them if they lead to articles
        for next_page in response.css('a::attr(href)').getall():
            if next_page and 'article' in next_page:                        # Only follow links that have 'article' in their URL
                yield response.follow(next_page, callback=self.parse)       # Follow the link and repeat the scraping
