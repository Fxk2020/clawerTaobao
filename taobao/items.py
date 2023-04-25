# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # img_src = scrapy.Field()
    title = scrapy.Field()  # 商品名
    prize = scrapy.Field()  # 商品价格
    content = scrapy.Field()  # 商品详情
    people_buy = scrapy.Field()  # 商品购买人数
    shop_name = scrapy.Field()  # 店铺名称
    shop_url = scrapy.Field()  # 店铺url
    item_type = scrapy.Field()  # 商品种类

