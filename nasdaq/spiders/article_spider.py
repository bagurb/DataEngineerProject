import scrapy
import os
import random

from ..items import NasdaqItem
class NasdaqSpiderSpider(scrapy.Spider):
    name = 'article_spider'
    dirname = os.path.dirname(__file__)
    f = open(os.path.join(dirname,"urls","urls.txt"))
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    USER_AGENT_LIST = ["Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
    ]
    
    custom_settings = { 
    'USER_AGENT': random.choice(USER_AGENT_LIST),
    'ROBOTSTXT_OBEY' : 'False',
    'FEED_URI' : 'Datas/article.json',
    'FEED_FORMAT' : 'json',
    'FEED_EXPORT_ENCODING' : 'utf-8',
    'DOWNLOAD_DELAY' : '0.25' }

    def parse(self, response):
        item=NasdaqItem()
        if(str(response.request.url).startswith('https://www.lemondeinformatique.fr')):
            links = response.css('h2 a::attr(href)').getall()
            for url in set(links):
                society = response.css('h1::text').getall()
                item['society'] = society
                url = response.urljoin(url)
                yield scrapy.Request(url,callback=self.parse_article_info,meta={'nasdaqItem':item})
        elif(str(response.request.url).startswith('https://www.usine-digitale.fr')):
            links = response.css('.titreBlocResultRech::attr(href) ').getall()
            for url in set(links):
                society = response.css('span.termRchch::text').getall()
                item['society'] = society
                url = response.urljoin(url)
                yield scrapy.Request(url,callback=self.parse_article_usine,meta={'nasdaqItem':item})

    def parse_article_info(self,response):
        item=response.meta.get('nasdaqItem')
        item['title']  = response.css('#article0 h1::text').getall()
        item['text']  = response.css('.article-body, .description').css('::text').getall()
        item['link'] = response.request.url
        yield item

    def parse_article_usine(self,response):
        item=response.meta.get('nasdaqItem')
        item['title']  = response.css('.titreType2::text').getall()
        item['text']  = response.css('.blocTexteType1 p , .chapoType4').css('::text').getall()
        item['link'] = response.request.url
        
        yield item