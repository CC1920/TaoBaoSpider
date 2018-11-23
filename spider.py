import requests
import re
import json
import time
import pymysql


def get_code(goods, page):
    url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&' \
          'ie=utf8&' \
          'spm=a21bo.2017.201856-taobao-item.2&' \
          'sourceId=tb.index&' \
          'search_type=item&' \
          'ssid=s5-e&' \
          'commend=all&' \
          'imgfile=&' \
          'q={}' \
          'suggest=history_1&' \
          '_input_charset=utf-8&' \
          'wq=&' \
          'suggest_query=&' \
          'source=suggest&' \
          'bcoffset=3&' \
          'ntoffset=0&' \
          'p4ppushleft=1%2C48&' \
          's={}'.format(goods, page)

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
        'cookie': '',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers).text
        pattern = re.compile(r'g_page_config = ({.*?});', re.S)
        content = pattern.findall(response)
        info = json.loads(content[0])
        clear_info = info['mods']['itemlist']['data']['auctions']
        price = [clear_info[i]['view_price'] for i in range(len(clear_info))]
        pay_people = [clear_info[i]['view_sales'] for i in range(len(clear_info))]
        des = [clear_info[i]['raw_title'] for i in range(len(clear_info))]
        shop = [clear_info[i]['nick'] for i in range(len(clear_info))]
        city = [clear_info[i]['item_loc'] for i in range(len(clear_info))]
        return price, pay_people, des, shop, city
    except Exception:
        return '获取第{}页数据错误，正在准备爬{}页的数据'.format(page, page+1)

def save_in_sql(goods, page):
    try:
        info = get_code(goods, page)
        index = 0
        while index < len(info[0]):
            '''
            因为获取数据是根据类别分类的，比如价格，商铺名字等，而存入数据库的时候，是依次存的
            所以这里用一个 列表b 来保存每一个需要的信息，再分别 存入数据库
            因为是循环，所以每次提取完一个完整的信息并且存入数据库后，就删掉列表，重新获取下一个信息
            '''
            b = []
            for i in info:
                b.append(i[index])
            print('准备插入的关键信息：', b)
            db = pymysql.connect('localhost', 'root', 'zxczxc', 'taobao')
            cursor = db.cursor()
            print('正在插入数据')
            sql = "insert into fuck(goods, price, pay_people, des, shop_name, city)" \
                    " values ('{}', '{}', '{}','{}','{}', '{}')".format(goods, b[0], b[1][:-3], b[2], b[3], b[4])
            try:
                cursor.execute(sql)
                print('数据插入成功')
                db.commit()
            except:
                db.rollback()
                return '数据插入发生错误'
            finally:
                db.close()
            index += 1
            del b

    except Exception:
        return '没有获取到数据等待几秒'



goods = input('请输入你想要查询的商品：')


for page in range(44, 4400, 44):
    save_in_sql(goods, page)
    time.sleep(5)




