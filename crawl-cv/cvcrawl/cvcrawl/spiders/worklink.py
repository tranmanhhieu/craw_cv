import scrapy
import re
import datetime

class CVProfile(scrapy.Spider):

    name = "worklink"
    allowed_domains = ['worklink.vn']
    start_urls = ['https://worklink.vn/candidate-listing/']

    def start_requests(self):
        for i in range(1,2):
            yield scrapy.Request(url=f'https://worklink.vn/candidate-listing/?ajax_filter=true&candidate_page={str(i)}',
                                 callback=self.parse_full_link)
        # yield scrapy.Request(url=f'https://worklink.vn/candidate-listing/?ajax_filter=true&candidate_page=1',
        #                      callback=self.parse_full_link)
    def parse_full_link(self, response):
        links = response.xpath('//*/ul/li/div/div[2]/div/h2/a/@href').getall()
        for url in links:
            yield scrapy.Request(url= url, callback=self.parse)
        # yield scrapy.Request(url='https://worklink.vn/candidate/vu-tuan/', callback=self.parse)

    def parse(self, response):
        data = {}
        url = response.url
        data['duong_dan'] = url
        data['id'] = response.xpath('//*[@id="jobsearch-review-form"]/ul/li[5]/input[1]/@value').get()
        data['avatar'] = response.xpath('/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/figure/img/@src').get()
        data['ten'] = response.xpath('/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/h2/a/text()').get()

        list_txt = response.xpath('/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/p/text()|/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/span[2]/text()').getall()
        for li in  list_txt:
            if li == list_txt[0]:
                data['vi_tri_ung_tuyen'] = li
            elif "Ngành" in li:
                data['nganh'] = li.split(':')[1]
            elif "Lương" in li:
                data['luong'] = li.split(':')[1]
            elif "Tuổi" in li:
                data['tuoi'] = li.replace(')','').split(':')[1]
            elif "Việt" in li:
                data['dia_chi'] = li

        data['ngay_tao_ho_so'] = response.xpath('/html/body/div[2]/div[4]/div/div/div/aside/div[1]/div/small/text()').get().split(',')[1]

        list_product1 = response.xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[1]/div[2]/ul/li/div/span/text()').getall()
        list_product2 = response.xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[1]/div[2]/ul/li/div/small/text()').getall()
        for i in range(0,4):
            data[list_product1[i]] = list_product2[i]

        muc_tieu = response.xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[1]/div[@class="jobsearch-description"]/p/text()').getall()
        if muc_tieu is not None:
            data['muc_tieu_nghe_nghiep'] = muc_tieu
        else:
            data['muc_tieu_nghe_nghiep'] = -1

        ky_nang = response.xpath('/html/body/div[2]/div[4]/div/div/div/div/div/div[@class ="jobsearch-jobdetail-tags"]/a/text()').getall()
        if ky_nang is not None:
            data['ky_nang'] = [i.strip() for i in ky_nang]
        else:
            data['ky_nang'] = -1

        title = response.xpath('//div[@class="jobsearch-candidate-title"]/h2/text()').getall()
        titl = [tit.strip() for tit in title if tit.strip() != '']

        timelines = response.xpath('//div[@class="jobsearch-candidate-timeline"]/ul')
        list_time = []
        for i in timelines:
            list_li = i.xpath('./li')
            time = []
            for li in list_li:
                text = li.xpath('./*//text()').getall()
                time.append(' '.join([tx.strip() for tx in text if tx.strip() != '']))
            list_time.append('|'.join(time))
        print(titl)
        if 'Giáo dục' in titl:
            data['giao_duc'] = list_time[0]
        else:
            data['giao_duc'] = -1

        if 'Kinh nghiệm' in titl:
            data['kinh_nghiem'] = list_time[1]
        else:
            data['kinh_nghiem'] = -1


        print(data)
        # yield data


