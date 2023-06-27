import scrapy


# class ExampleSpider(scrapy.Spider):
    # name = 'yg'
    # allowed_domains = ['sun0769.com']
    # start_urls = ['http://wz.sun0769.com/index.php/question/report']
    #
    # def parse(self, response):
    #     tr_list = response.xpath("//div[@class='greyframe']/table[2]//tr")
    #     for tr in tr_list:
    #         item = YangguangItem()
    #         item["title"] = tr.xpath("./td[2]/a[2]/text()").extract_first()
    #         item["href"] = tr.xpath("./td[2]/a[2]/@href").extract_first()
    #         item["status"] = tr.xpath("./td[3]/span/text()").extract_first()
    #         item["publish_time"] = tr.xpath("./td[last()]/text()").extract_first()
    #         if type(item["href"]) == str:
    #             # 请求详情页
    #             yield scrapy.Request(
    #                 item["href"],
    #                 callback=self.parse_detail,
    #                 meta={"item": item}
    #             )
    #
    #     # 翻页
    #     next_url = response.xpath("//a[text()='>']/@href").extract_first()
    #     if next_url is not None:
    #         yield scrapy.Request(next_url, callback=self.parse)
    #
    # # 解析详情页
    # def parse_detail(self, response):
    #     item = response.meta["item"]
    #     # 获取详情页的内容、图片
    #     item["content"] = response.xpath("//div[@class='wzy1']/table[2]//tr[1]/td[@class='txt16_3']/text()").extract()
    #     item["content_image"] = response.xpath(
    #         "//div[@class='wzy1']/table[2]//tr[1]/td[@class='txt16_3']//img/@src").extract()
    #     item["content_image"] = ["http://wz.sun0769.com" + i for i in item["content_image"]]
    #     yield item  # 对返回的数据进行处理