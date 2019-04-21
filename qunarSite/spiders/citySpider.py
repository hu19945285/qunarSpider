# -*- coding: utf-8 -*-
import scrapy
from ..items import QunarcityItem

class CityspiderSpider(scrapy.Spider):
    name = 'citySpider'
    #构造请求头
    allow_domains=['http://travel.qunar.com']
    start_urls=[
            "http://travel.qunar.com/place/"
            ]
        
    def parse(self, response):
        provinces = response.xpath("//div[@class = 'sub_list']")
        for city in provinces[0].xpath(".//li"):        #直辖市
            item = QunarcityItem()
            item['city_name']=city.xpath("./a/text()").extract_first()
            item['province_name']=item['city_name']
            item['city_httpsite']=city.xpath("./a/@href").extract_first() #city的http地址
            item['city_id']=city.xpath("./a/@href").extract_first().split('-')[1]
            yield item
        for province in provinces[1:]:  #除了直辖市外的其他省份
            for city in province.xpath(".//li"):
                item = QunarcityItem()
                item['city_name']=city.xpath("./a/text()").extract_first()
                item['city_httpsite']=city.xpath("./a/@href").extract_first()
                item['city_id']=city.xpath("./a/@href").extract_first().split('-')[1]
                item['province_name']="".join(province.xpath("./div[@class='titbox']/span/text()").extract_first().split())[:-1]
                yield item
                 
