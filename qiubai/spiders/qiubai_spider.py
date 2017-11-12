# coding: UTF-8

from scrapy import Request
from scrapy.spiders import Spider
from qiubai.items import QiubaiItem
from qiubai import const


class qiubai_spider(Spider):
	name = "qiubai_spider"
	start_urls = ['https://www.qiushibaike.com/']
	# def start_request(self,url):
	# 	url = 'https://www.qiushibaike.com/hot'
	# 	yield Request(url,callback= self.parse)

	def parse(self,response):
		domain = 'https://www.qiushibaike.com'
		article_iterator = response.xpath('//div[@id="content-left"]/div[contains(@class,"article block")]')
		for article in article_iterator:
			item = QiubaiItem()
			_id = article.xpath('.//@id').extract_first()
			item['_id'] = _id
			try:
				item['_type'] = article.xpath('.//@class').extract_first()
				item['_author'] = article.xpath('.//div[@class="author clearfix"]/a[1]/img/@alt').extract_first()
				item['_avatar'] = article.xpath('.//div[@class="author clearfix"]/a[1]/img/@src').extract_first()
				item['_url'] = article.xpath('.//a[contains(@href,"article")]/@href').extract_first()
				item['_content'] = article.xpath('.//a/div[@class="content"]/span/text()').extract_first()
				item['_like'] = article.xpath('.//div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract_first()
				item['_status'] = const.SPIDER_STATUS_FINISHED
			except Exception, e:
				item['_status'] = const.SPIDER_STATUS_FAILED
				self.logger.error('parse item error:%r',e)
			self.logger.info('parse item:%r',item)
			yield item