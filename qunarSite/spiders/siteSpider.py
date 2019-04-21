# -*- coding: utf-8 -*-
import scrapy
from ..items import QunarsiteItem
import pytesseract
from PIL import Image
from io import BytesIO
import requests
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
 
meta_ex={
    'dont_redirect':True,
    'handle_httpstatus_list': [302]
  }



class SitesSpider(scrapy.Spider):
    name = 'siteSpider'

    #构造请求头
    start_urls=[
            "http://travel.qunar.com/place/"
            ]
        
    def parse(self, response):      #爬取每一个城市下的主页面
        '''
        cityspots_url='http://travel.qunar.com/p-cs299782-xiamen-jingdian'
        yield scrapy.Request(cityspots_url,callback=self.parse_citysites)
        
        '''
        provinces = response.xpath("//div[@class = 'sub_list']")
        for city in provinces[0].xpath(".//li"):        #直辖市
            cityspots_url=city.xpath("./a/@href").extract_first()+'-jingdian'
            yield scrapy.Request(cityspots_url,meta=meta_ex,callback=self.parse_citysites)
            yield scrapy.Request(cityspots_url+'-1-2',meta=meta_ex,callback=self.parse_citysites)
            yield scrapy.Request(cityspots_url+'-1-3',meta=meta_ex,callback=self.parse_citysites)
            yield scrapy.Request(cityspots_url+'-1-4',meta=meta_ex,callback=self.parse_citysites)
            yield scrapy.Request(cityspots_url+'-1-5',meta=meta_ex,callback=self.parse_citysites)
            yield scrapy.Request(cityspots_url+'-1-6',meta=meta_ex,callback=self.parse_citysites)
        for province in provinces[1:]:  #除了直辖市外的其他省份
            for city in province.xpath(".//li"):
                cityspots_url=city.xpath("./a/@href").extract_first()+'-jingdian'
                yield scrapy.Request(cityspots_url,meta=meta_ex,callback=self.parse_citysites)
                yield scrapy.Request(cityspots_url+'-1-2',meta=meta_ex,callback=self.parse_citysites)
                yield scrapy.Request(cityspots_url+'-1-3',meta=meta_ex,callback=self.parse_citysites)
                yield scrapy.Request(cityspots_url+'-1-4',meta=meta_ex,callback=self.parse_citysites)
                yield scrapy.Request(cityspots_url+'-1-5',meta=meta_ex,callback=self.parse_citysites)
                yield scrapy.Request(cityspots_url+'-1-6',meta=meta_ex,callback=self.parse_citysites)               

        pass

    def parse_citysites(self,response):       #爬取一个城市里的所有景点的列表
        '''
        pic_src=response.xpath(".//img/@src").extract_first()
        if 'http://travel.qunar.com/space/captcha' in pic_src:
            img=requests.get(pic_src)
            image = Image.open(BytesIO(img.content))
            image=image.convert('L')
            code=pytesseract.image_to_string(image)
            formdata={
                    'code':code
                    }
            url="travel.qunar.com/space/captcha/verify"
            yield scrapy.FormRequest(url=url,formdata=formdata,callback=self.parse_citysites,dont_filter=True)
        '''    
        spots = response.xpath(".//ul[@class = 'list_item clrfix']//li")
        for spot in spots:
            spot_url=spot.xpath("./a/@href").extract_first()
            request=scrapy.Request(spot_url,meta=meta_ex,callback=self.parse_spot)
            request.meta['city_id']=response.url.split('-')[1]
            yield request
        
        
        
        '''
            nextpage_url=response.xpath(".//div[@class='b_paging']/a[@class='page next']/@href").extract_first()
            if nextpage_url:
                yield scrapy.Request(nextpage_url)
                              
        '''
        pass
    
    def parse_spot(self,response):             #爬取一个景点的信息
        '''
        pic_src=response.xpath(".//img/@src").extract_first()
        if 'http://travel.qunar.com/space/captcha' in pic_src:
            img=requests.get(pic_src)
            image = Image.open(BytesIO(img.content))
            image=image.convert('L')
            code=pytesseract.image_to_string(image)
            formdata={
                    'code':code
                    }
            url="travel.qunar.com/space/captcha/verify"
            yield scrapy.FormRequest(url=url,formdata=formdata,callback=self.parse_spot,dont_filter=True)
        '''
        item=QunarsiteItem()
        item['spot_id']=response.url.split('-')[1]
        item['spot_name']=response.xpath(".//h1[@class='tit']/text()").extract_first()
        item['spot_cityId']=response.meta['city_id']
        item['spot_rank']=response.xpath(".//div[@class='ranking']/span/text()").extract_first()
        item['spot_intro']= response.xpath(".//div[@class='e_db_content_box']//p").extract_first()      #[0].xpath("./text()").extract_first()
        item['spot_playTime']=response.xpath(".//div[@class='time']/text()").extract_first()#.split('：')[1]
        item['spot_grade']=response.xpath(".//div[@class='scorebox clrfix']/span[@class='cur_score']/text()").extract_first()
        item['spot_addr']=response.xpath(".//div[@class='e_summary_list clrfix']/table/tr/td[1]/dl[1]//span/text()").extract_first()
        item['spot_tel']=response.xpath(".//div[@class='e_summary_list clrfix']/table/tr/td[1]/dl[2]//span/text()").extract_first()
        item['spot_openTime']= response.xpath(".//div[@class='e_summary_list clrfix']/table/tr/td[2]/dl//span/p/text()").extract_first()
        item['spot_ticket']='0'
        item['spot_visitSeason']=response.xpath(".//div[@class='b_detail_section b_detail_travelseason']/div[@class='e_db_content_box e_db_content_dont_indent']/p/text()").extract_first()
        item['spot_trafficGuide']=response.xpath(".//div[@class='b_detail_section b_detail_traffic']//p").extract_first()
        item['spot_commentsNum']=response.xpath(".//div[@class='b_detail_section b_detail_comment']//h3[@class='e_title_content']/span/text()").re('\d+')
        if(item['spot_commentsNum']):
            item['spot_commentsNum']=item['spot_commentsNum'][0]
        item['spot_5starNum']=int(int(item['spot_commentsNum'])*int(response.xpath(".//div[@class='star-top']/ul//div[@class='rate']")[0].xpath("@style").re('\d+')[0])*0.01)
        item['spot_4starNum']=int(int(item['spot_commentsNum'])*int(response.xpath(".//div[@class='star-top']/ul//div[@class='rate']")[1].xpath("@style").re('\d+')[0])*0.01)
        item['spot_3starNum']=int(int(item['spot_commentsNum'])*int(response.xpath(".//div[@class='star-top']/ul//div[@class='rate']")[2].xpath("@style").re('\d+')[0])*0.01)
        item['spot_2starNum']=int(int(item['spot_commentsNum'])*int(response.xpath(".//div[@class='star-top']/ul//div[@class='rate']")[3].xpath("@style").re('\d+')[0])*0.01)
        item['spot_1starNum']=int(int(item['spot_commentsNum'])*int(response.xpath(".//div[@class='star-top']/ul//div[@class='rate']")[4].xpath("@style").re('\d+')[0])*0.01)
        item['spot_5starNum']=str(item['spot_5starNum'])
        item['spot_4starNum']=str(item['spot_4starNum'])
        item['spot_3starNum']=str(item['spot_3starNum'])
        item['spot_2starNum']=str(item['spot_2starNum'])
        item['spot_1starNum']=str(item['spot_1starNum'])
        '''
        item['spot_goodComNum']=
        spot_mediComNum=scrapy.Field()
        spot_badComNum=scrapy.Field()
        '''
        yield item
        pass