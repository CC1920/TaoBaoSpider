# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree
import re
import time
import json
from daxi.urtils import drag_and_drop

class ZhaodaxiSpider(scrapy.Spider):
    name = 'zhaodaxi'
    allowed_domains = ['zhaodaxi.taobao.com']
    start_urls = ['http://zhaodaxi.taobao.com/']

    def parse(self, response):
        url = 'https://zhaoyandaxi.taobao.com/search.htm?spm=a1z10.1-c-s.w15674828-14439897244.4.16786eabhYzh0p&scene=taobao_shop'
        headers = {
            'authority': 's.taobao.com',
            'method': 'GET',
            'path': '/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E7%94%B5%E8%84%91&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=132',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'referer': 'https://www.taobao.com/?spm=a1z02.1.1581860521.1.51a0782d8r4hBm',
            # 'cookie': 'miid=100826399472139206; t=caae9a630df4a368b2a748641c5a0c7a; cna=dxtHFL/A+i8CAXWgi/1DVvV5; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; tg=0; enc=EEG814gfavdyzPsGaOwBnooH3zfDogqijbXHuck%2BkkyKQG%2BIQgMmgU1bUemJfD0RFZSeaZAdQPV28Ws6uAEqxQ%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1; cookie2=10c03a913646d2b9ade712ed10ceb540; _tb_token_=fe96837817eee; swfstore=116572; UM_distinctid=1674dd2d6350-0464b893d8cb42-8383268-1fa400-1674dd2d637163; v=0; unb=2330824444; sg=%E8%82%8946; _l_g_=Ug%3D%3D; skt=1be1c2661ada9c7e; cookie1=BqbkvouTpWDxo43LUIxtiNqsPH1p3D5v%2FtIw4FgnU5o%3D; csg=681a9d28; uc3=vt3=F8dByR6kOHNL6isDcus%3D&id2=UUtIFZj3kt5%2Bfw%3D%3D&nk2=o%2FMlgcuziKysbb8C&lg2=W5iHLLyFOGW7aA%3D%3D; existShop=MTU0MzIxNDU0Ng%3D%3D; tracknick=%5Cu674E%5Cu6587%5Cu6587%5Cu7231%5Cu5403%5Cu8089; lgc=%5Cu674E%5Cu6587%5Cu6587%5Cu7231%5Cu5403%5Cu8089; _cc_=V32FPkk%2Fhw%3D%3D; dnk=%5Cu674E%5Cu6587%5Cu6587%5Cu7231%5Cu5403%5Cu8089; _nk_=%5Cu674E%5Cu6587%5Cu6587%5Cu7231%5Cu5403%5Cu8089; cookie17=UUtIFZj3kt5%2Bfw%3D%3D; pnm_cku822=098%23E1hvuQvUvbpvUvCkvvvvvjiPR2MU1jY8R2LUQjD2PmPZgjYnRsMvljEjR2cvQjE22QhvCvvvMM%2FivpvUphvh5oN9CRkEvpvVpyUUCCKwKphv8hCvvvvvvhCvphvwv9vvp%2FDvpCQmvvChNhCvjvUvvhBZphvwv9vvBHpEvpCWpSL3v8RNayHQpRFw5CD1cLXXiXhpVj%2BOUx8x9CQaWDw6pwethbUf85yyYE7rejyy465XifVA2oY%2BCNLOVBrgx2XXiXhpVj%2BOUx8x9vhCvvXvppvvvvvtvpvhphvvv8wCvvBvpvpZ; uc1=cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=UIHiLt3xTIkz&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTYNclEwhzzsQ%3D%3D&tag=8&lng=zh_CN; mt=ci=35_1; isg=BD4-QLhf6RJRWz0h_c8xY3uRj1RA1zZhemkZB-hHggF8i99lUgwdCF0qBxfis_oR; whl=-1%260%260%261543214584161',
            'upgrade-insecure-requests': '1',
            'user - agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 69.0.3497.100Safari / 537.36'
        }
        try:
            response = requests.get(url, headers=headers).text
            code = etree.HTML(response)
            # 前面的“所有宝贝”--“本周新品”--“17，18 新品”，后面的“清仓-秒发-邮费链接” 这里不需要,从dress-shoes
            # 取出所有分类的href
            goods_href = code.xpath('//div[@id="shop14439897285"]//ul/li//a/@href')[50:-4]
            for tag in goods_href:
                each_url = 'https:' + tag
                # 因为分类包含所有细的分类，所以只取细的分类
                if len(each_url) > 114:
                    each_page_reponse = requests.get(each_url, headers=headers).headers['url-hash']
                    yield each_page_reponse
        except Exception:
            return '没有获取到任何数据，请重新测试'


    def parse_code(self):
        for category in :
            # 只提取每一个商品分类的 id
            pattern = re.compile('\d{9,}', re.S)
            category_id = re.findall(pattern, category)
            s = str(time.time())
            s1 = s.replace('.', '')[:13]
            url = 'https://zhaoyandaxi.taobao.com/i/asynSearch.htm?&_ksTS={}_150callback=jsonp151&mid=w-14439897311-0&wid=14439897311&' \
                  'path=/category-{id}.htm&catId={id}&scid={id}'.format(s1, id=category_id[0])
            headers = {
                'authority': 'zhaoyandaxi.taobao.com',
                'method': 'GET',
                'scheme': 'https',
                'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
                'accept - encoding': 'gzip, deflate, br',
                'accept - language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
                'cache - control': 'max - age = 0',
                'upgrade - insecure - requests': '1',
                'user - agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                'cookie': 'miid=100826399472139206; t=caae9a630df4a368b2a748641c5a0c7a; cna=dxtHFL/A+i8CAXWgi/1DVvV5; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; tg=0; enc=EEG814gfavdyzPsGaOwBnooH3zfDogqijbXHuck%2BkkyKQG%2BIQgMmgU1bUemJfD0RFZSeaZAdQPV28Ws6uAEqxQ%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1; UM_distinctid=1674dd2d6350-0464b893d8cb42-8383268-1fa400-1674dd2d637163; _cc_=V32FPkk%2Fhw%3D%3D; mt=ci=0_0; v=0; cookie2=118e95611901f54abd9fe4e136485b4e; _tb_token_=faee55145119d; uc1=cookie14=UoTYNclMDoWf4w%3D%3D; pnm_cku822=098%23E1hvIvvUvbpvUvCkvvvvvjiPR2MWQjt8PsMyzjD2PmP90jEhR2qpsjr2R2cwQj3PkphvCyEmmvpf58yCvv3vpvoa83XLEfyCvm3vpvvvvvCvphCvjvUvvhjRphvwv9vvBj1vpCQmvvChxhCvjvUvvhBZmphvLhEnEQmFHFXX8Z0vQE01UxUDCaFIRfU6pLEw9E7rejyyNB3r1CkKf96IowynrsUDX2pwD70Oe166fvDr1EuKNZD1B5exdX3tEVQEfwpCvpvVph9vvvvv2QhvCvvvMMGtvpvhphvvv8wCvvBvpvpZ; isg=BBgYtyT19wdwatuT54H_0WG36UZqqUgTME__1VIJRtMG7bjX-hSzGy_MIWX4fTRj'
            }
            print('正在爬取的网页')
            print(url)
            r = requests.get(url, headers=headers).text
            try:
                yanzheng_url = json.loads(r)['url']
                if yanzheng_url:
                    drag_and_drop(yanzheng_url)
            except Exception:
                return '什么错误'
            else:
                return r


