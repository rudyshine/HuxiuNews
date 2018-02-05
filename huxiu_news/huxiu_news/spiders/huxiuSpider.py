import scrapy
from huxiu_news.items import HuxiuNewsItem
from selenium import webdriver
import time
from bs4 import BeautifulSoup


class HuxiuSpider(scrapy.Spider):
    # Spider的名称
    name = 'huxiu'
    # 爬取的url
    start_urls = ['https://www.huxiu.com/channel/104.html']

    def parse(self, response):
        """
        解析页面的响应数据，因为解析的数据比较多，使用yield关键字，将怎个方法作为生成器，迭代获取解析的数据
        :param response: 响应的数据
        :return:
        """
        browser=webdriver.Chrome()
        browser.get(self.start_urls[0])
        js = "var q=document.documentElement.scrollTop=30000"

        for i in range(5):
            browser.execute_script(js)
            load =browser.find_element_by_xpath('//*[@id="index"]/div[1]/div[3]').click()
            time.sleep(3)
            print(i)
        sreach_windoe=browser.current_window_handle
        # 解析列表，获取当前页面所有的列表数据
        for sele in response.xpath('//div[@class="mob-ctt"]'):
            # 创建item对象
            item = HuxiuNewsItem()
            item['link']=sele.xpath('.//h2/a/@href')[0].extract()
            url='https://www.huxiu.com'+item['link']
            print(url)
            time.sleep(5)
            # yield scrapy.Request(url,callback=self.pares_article)

    def pares_article(self,response):
        item = HuxiuNewsItem()
        item['linkurl']=response.url
        print(item['linkurl'])
        for sele in response.xpath('//div[@class="article-section-wrap"]'):
            #将文本信息，赋值给item
            item['title'] = sele.xpath(".//h1/text()")[0].extract().strip()# 获取到标题的标签的文本数据
            print(item['title'])
            item['author'] =sele.xpath('.//*[@class="author-name"]/a/text()')[0].extract() # 获取文本数据author-name
            print(item['author'])
            item['content'] = sele.xpath('//*[@class="article-content-wrap"]/p/text()').extract()  # 获取到摘要的文本数据
            print(item['content'])
            yield item