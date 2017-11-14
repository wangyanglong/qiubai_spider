# --*-- coding: utf-8 --*--

from scrapy import Request
from scrapy.spiders import Spider
from qiubai.items import QiubaiItem
from qiubai import const
from urlparse import urljoin
import time

class qiubai_spider(Spider):
	name = "qiubai_spider"
	start_urls = ['https://www.qiushibaike.com/hot','https://www.qiushibaike.com/history/','https://www.qiushibaike.com/text/']
	# def start_request(self,url):
	# 	url = 'https://www.qiushibaike.com/hot'
	# 	yield Request(url,callback= self.parse)

	def parse(self,response):
		domain = 'https://www.qiushibaike.com/hot'
		article_iterator = response.xpath('//div[@id="content-left"]/div[contains(@class,"article block")]')
		for article in article_iterator:
			item = QiubaiItem()
			item['_qid'] = article.xpath('.//@id').extract_first()
			item['_update'] = int(time.time())
			try:
				item['_type'] = article.xpath('.//@class').extract_first()
				try:
					item['_author'] = article.xpath('.//div[@class="author clearfix"]/a[1]/@href').extract_first()
				except Exception,e:
					log.error("item parse author id error:%r",e)
				try:
					item['_pic'] = article.xpath('.//div[@class="thumb"]/a/img/@src').extract_first()
				except Exception,e:
					log.error("try to parse articel pic error:%r",r)
				item['_url'] = article.xpath('.//a[contains(@href,"article")]/@href').extract_first()
				item['_content'] = article.xpath('.//a/div[@class="content"]/span/text()').extract_first()
				item['_like'] = article.xpath('.//div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract_first()
				item['_status'] = const.SPIDER_STATUS_FINISHED
			except Exception, e:
				item['_status'] = const.SPIDER_STATUS_FAILED
				self.logger.error('parse item error:%r',e)
			yield item
		next_iterator = response.xpath('//*[@id="content-left"]/ul/li')
		for page in next_iterator:
			if page.xpath('.//a/span[@class="next"]').extract_first():
				next_page = urljoin(domain,page.xpath('.//a/@href').extract_first())
				self.logger.info('page:%r,next_page:%r',u'下一页',next_page)
				time.sleep(5)
				yield Request(next_page, callback=self.parse)