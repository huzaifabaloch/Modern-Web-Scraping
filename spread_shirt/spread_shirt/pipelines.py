# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request



class SpreadShirtPipeline(ImagesPipeline):
    """
        Overriding few methods in ImagePipeline class to set the name of image
        as name of the item ( By default -> random sha hexa digits )
    """

    def get_media_requests(self, item, info):
        """
            Here we are having the item field which is come from items class
            and here we grab each item ( item_name field )
        """
        return [Request(x, meta={'item_name': item.get('item_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        """
            Here are getting that item_name from get_media_requests to set the
            image name as whatever the item name is for each image.
        """
        return 'full/%s.jpg' % (request.meta['item_name'])
