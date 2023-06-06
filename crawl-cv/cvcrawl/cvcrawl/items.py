# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CvcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    duong_dan = scrapy.Field()
    id = scrapy.Field()
    avatar =scrapy.Field()
    ten = scrapy.Field()
    vi_tri_ung_tuyen = scrapy.Field()
    nganh = scrapy.Field()
    luong = scrapy.Field()
    tuoi = scrapy.Field()
    dia_chi = scrapy.Field()
    ngay_tao_ho_so = scrapy.Field()
    muc_tieu_nghe_nghiep = scrapy.Field()
    ky_nang = scrapy.Field()

