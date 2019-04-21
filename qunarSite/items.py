# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarcityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name=scrapy.Field()
    province_name=scrapy.Field()
    city_httpsite=scrapy.Field()
    city_id=scrapy.Field()
    pass

class QunarsiteItem(scrapy.Item):
    spot_id=scrapy.Field()
    spot_name=scrapy.Field()
    spot_cityId=scrapy.Field()
    spot_rank=scrapy.Field()
    spot_intro=scrapy.Field()
    spot_playTime=scrapy.Field()
    spot_grade=scrapy.Field()
    spot_addr=scrapy.Field()
    spot_tel=scrapy.Field()
    spot_openTime=scrapy.Field()
    spot_ticket=scrapy.Field()
    spot_visitSeason=scrapy.Field()
    spot_trafficGuide=scrapy.Field()
    spot_commentsNum=scrapy.Field()
    spot_5starNum=scrapy.Field()
    spot_4starNum=scrapy.Field()
    spot_3starNum=scrapy.Field()
    spot_2starNum=scrapy.Field()
    spot_1starNum=scrapy.Field()
    '''
    spot_goodComNum=scrapy.Field()
    spot_mediComNum=scrapy.Field()
    spot_badComNum=scrapy.Field()
    '''
    pass