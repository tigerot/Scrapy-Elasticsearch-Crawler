from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from datetime import datetime
from crawler.items import CrawlerItem

class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["sozcu.com.tr"]
    start_urls = ["https://www.sozcu.com.tr/"]

    rules = (
        Rule(LinkExtractor(allow=""), callback = "parse_item"),
    )

    def parse_item(self, response):
        #articles = response.css(".news-card")
        #for article in articles:
        #    raw_title = article.css(".news-card-footer::text").get()
        #    cleaned_title = re.sub(r'\s+', ' ', raw_title).strip() if raw_title else None
        #    href = article.css(".news-card-footer::attr(href)").get()
        #    if cleaned_title and href:
        #        yield {
        #            "title": cleaned_title,
        #            "link": response.urljoin(href),
        #            "timestamp": datetime.utcnow().isoformat() + 'Z'
        #    }
        for article in response.css('.news-card'):
            item = CrawlerItem()
            item['title'] = re.sub(r'\s+', ' ', article.css('.news-card-footer::text').get()).strip()
            item['link'] = response.urljoin(article.css('.news-card-footer::attr(href)').get())
            item['timestamp'] = datetime.utcnow().isoformat()  # ISO formatında zaman damgası
            yield item