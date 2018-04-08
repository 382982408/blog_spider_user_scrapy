# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from blogspider.items import BlogspiderItem


class SuperchaoSpider(scrapy.Spider):
    name = 'superchao'
    allowed_domains = ['www.66super.com']
    start_urls = ['http://www.66super.com/index.html']

    def parse(self,response):
        #处理每页的url
        post_nodes = response.xpath('//a[@class="mytitle"]')
        for each_node in post_nodes:
            article_url = parse.urljoin(response.url,each_node.xpath('@href').extract_first(""))
            yield Request(url=article_url, callback=self.parse_detail)


        #获取下一页，并会掉处理每页信息的url
        next_url = response.xpath('//ul[@class="pagination pagination-sm"]/li[last()-1]/a/@href').extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url), callback=self.parse)


    def parse_detail(self, response):
        title =  response.xpath('//*[@id="index_view"]/h1/text()').extract()[0]
        content =  '\n'.join(response.xpath('//*[@id="index_view"]/ul/span/p/text()').extract())

        print(title)
        print(content)

        blog_item = BlogspiderItem()

        blog_item["title"] = title
        blog_item["content"] = content

        yield blog_item


