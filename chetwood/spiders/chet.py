import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from chetwood.items import Article


class ChetSpider(scrapy.Spider):
    name = 'chet'
    start_urls = ['https://chetwood.co/news/']

    def parse(self, response):
        links = response.xpath('//a[@class="singleNewsItem-module--asImage--1wQtp"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="newsItem-module--date--1N7qx"]/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d %B %Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="news-template"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
