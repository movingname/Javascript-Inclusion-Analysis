import scrapy

class JSSpider(scrapy.Spider):
    name = "js_spider"
    # Don't use *.uber.com.
    # allowed_domains = ["uber.com"]
    allowed_domains = ["instacart.com"]
    start_urls = [
        #"https://help.uber.com/",
        #"https://developer.uber.com/"
        "https://www.instacart.com",
        "https://partners.instacart.com",
        "https://shoppers.instacart.com"
    ]

    def parse(self, response):

        self.parse_js_links(response)
        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_js_links)

    def parse_js_links(self, response):
        # with open("data/uber.txt", 'a') as f:
        with open("data/instacart.txt", 'a') as f:
            f.write("Page:" + response.url + "\n")
            for sel in response.xpath('//script/@src'):
                f.write(sel.extract() + "\n")
                print(sel.extract())

