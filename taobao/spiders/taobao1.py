import time

import scrapy
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from taobao.items import TaobaoItem
from taobao.middlewares import TaobaoDownloaderMiddleware
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector

from taobao.settings import KEY_WORDS_FILE
from taobao.util import re_font, read_keywords


class Taobao1Spider(scrapy.Spider):
    name = "taobao1"
    allowed_domains = ["taobao.com"]

    now_keyword = ""
    page_now = 0
    page_number = 3 #100

    def start_requests(self):
        # keywords = read_keywords(KEY_WORDS_FILE)  # '笔记本电脑', '键盘', '鼠标', '耳机', '显示器', '音响'
        keywords = ['小米']  # '笔记本电脑', '键盘', '鼠标', '耳机', '显示器', '音响'
        for keyword in keywords:
            self.now_keyword = keyword
            for page in range(self.page_number):
                if page != 0:
                    time.sleep(15)
                url = f'https://s.taobao.com/search?page={page + 1}&q={keyword}&s={page * 48}'
                yield scrapy.Request(url)

    def parse(self, response):
        for number in range(48):
            item = TaobaoItem()
            # #root > div > div:nth-child(2) > div.PageContent--contentWrap--mep7AEm > div.LeftLay--leftWrap--xBQipVc >
            # div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child(4)
            item["content"] = response.css(
                f'#root > div > div:nth-of-type(2) > div.PageContent--contentWrap--mep7AEm > '
                f'div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > '
                f'div.Content--content--sgSCZ12 > div > div:nth-of-type({number + 1}) > a::attr(href)').get()
            sel = response.css(
                f'#root > div > div:nth-of-type(2) > div.PageContent--contentWrap--mep7AEm > '
                f'div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > '
                f'div.Content--content--sgSCZ12 > div > div:nth-of-type({number + 1}) > a > div')

            if sel.get() is not None:
                # #root > div > div:nth-child(2) > div.PageContent--contentWrap--mep7AEm > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div:nth-child(2) > a
                # a > div > div.Card--mainPicAndDesc--wvcDXaK > div.MainPic--mainPicWrapper--iv9Yv90 > img
                # div.Card--mainPicAndDesc--wvcDXaK > div.Title--descWrapper--HqxzYq0 > div > span
                fonts = sel.css('div.Card--mainPicAndDesc--wvcDXaK > div.Title--descWrapper--HqxzYq0 > div > '
                                        'span::text').extract()
                font_all = ""
                for font in fonts:
                    font_all += font
                # a > div > div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > span.Price--priceInt--ZlsSi_M
                item["title"] = font_all
                item["prize"] = sel.css('div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > '
                                        'span.Price--priceInt--ZlsSi_M::text').get()
                # div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > span.Price--realSales--FhTZc7U
                item['people_buy'] = sel.css('div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > '
                                             'span.Price--realSales--FhTZc7U::text').get()
                # div.ShopInfo--shopInfo--ORFs6rK > div.ShopInfo--TextAndPic--yH0AZfx > a
                item['shop_name'] = sel.css(
                    'div.ShopInfo--shopInfo--ORFs6rK > div.ShopInfo--TextAndPic--yH0AZfx > a::text').get()
                item['shop_url'] = sel.css(
                    'div.ShopInfo--shopInfo--ORFs6rK > div.ShopInfo--TextAndPic--yH0AZfx > a::attr(href)').get()
            else:
                sel2 = response.css(f'#mainsrp-itemlist > div > div > div:nth-of-type(1) > div:nth-of-type({number+1}) > div.ctx-box.J_MouseEneterLeave.J_IconMoreNew')
                # J_Itemlist_TLink_693157239888 > span.baoyou-intitle.icon-service-free
                # print(item['title'])
                fonts = sel2.css('div.row.row-2.title > a::text').extract()
                font_all = ""
                for font in fonts:
                    font_all += font
                if font_all != "":
                    font_all = re_font(font_all)
                    # print(font_all)
                    item["title"] = font_all
                    # a > div > div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > span.Price--priceInt--ZlsSi_M
                    item["prize"] = sel2.css('div.row.row-1.g-clearfix > div.price.g_price.g_price-highlight > '
                                             'strong::text').get()
                    # div.Card--mainPicAndDesc--wvcDXaK > div.Price--priceWrapper--Q0Dn7pN > span.Price--realSales--FhTZc7U
                    item['people_buy'] = sel2.css('div.row.row-1.g-clearfix > div.deal-cnt::text').get()
                    # div.ShopInfo--shopInfo--ORFs6rK > div.ShopInfo--TextAndPic--yH0AZfx > a
                    # > div.row.row-3.g-clearfix > div.shop > a > span:nth-child(2)
                    # div.row.row-3.g-clearfix > div.shop > a > span:nth-child(2)
                    item['shop_name'] = sel2.css('div.row.row-3.g-clearfix > div.shop > a > span:nth-of-type(2)::text').get()
                    item['shop_url'] = sel2.css('div.row.row-3.g-clearfix > div.shop > a::attr(href)').get()
            if item['title'] is None:
                continue
            item['item_type'] = self.now_keyword
            yield item
