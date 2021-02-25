import scrapy

from scrapy.loader import ItemLoader
from ..items import CaindosuezmcItem
from itemloaders.processors import TakeFirst


class CaindosuezmcSpider(scrapy.Spider):
	name = 'caindosuezmc'
	start_urls = ['https://ca-indosuez.com/fr/presse']

	def parse(self, response):
		post_links = response.xpath('//div[@id="press_release"]//a[@class="link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="block-articleTitle--title mb-30"]/h3/text()').get()
		description = response.xpath('//div[@class="block-wysiwg-text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="block-articleTitle--author mb-30"]/p/text()').get()

		item = ItemLoader(item=CaindosuezmcItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
