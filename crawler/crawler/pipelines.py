# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch
import logging


class CrawlerPipeline:
    def __init__(self, es_host, es_port, es_scheme, es_index):
        self.es_host = es_host
        self.es_port = es_port
        self.es_scheme = es_scheme
        self.es_index = es_index
        self.es_client = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            es_host=crawler.settings.get('ELASTICSEARCH_HOST', 'localhost'),
            es_port=crawler.settings.get('ELASTICSEARCH_PORT', 9200),
             es_scheme=crawler.settings.get('ELASTICSEARCH_SCHEME', 'http'),
            es_index=crawler.settings.get('ELASTICSEARCH_INDEX', 'sozcu-main-page')
        )

    def open_spider(self, spider):
        self.es_client = Elasticsearch([{'scheme': self.es_scheme, 'host': self.es_host, 'port': self.es_port}])
        logging.info(f"Connected to Elasticsearch at {self.es_scheme}://{self.es_host}:{self.es_port}")

    def close_spider(self, spider):
        if self.es_client:
            self.es_client.transport.close()

    def process_item(self, item, spider):
        try:
            # Elasticsearch'e belge ekle
            self.es_client.index(index=self.es_index, document=dict(item))
            logging.info(f"Document indexed in Elasticsearch: {item}")
        except Exception as e:
            logging.error(f"Error indexing document: {e}")
        return item
