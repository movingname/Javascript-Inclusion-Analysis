import scrapy
from selenium import webdriver

# We rely on scrapy to find and follow links, while we use selenium
# to extract data.

class JSSpider(scrapy.Spider):
    name = "js_spider"

    def __init__(self, site="instacart"):

        self.site = site
        self.driver = webdriver.Firefox()

        # Should not use something like *.uber.com.
        self.allowed_domains = []
        self.add_lines_from_file("../data/" + site + "_domains.txt", self.allowed_domains)

        self.start_urls = []
        self.add_lines_from_file("../data/" + site + "_seeds.txt", self.start_urls)

    def add_lines_from_file(self, filename, _list):
        with open(filename) as f:
            for line in f:
                url = line.strip()
                if url != "":
                    _list.append(url)

    def parse(self, response):

        self.get_js_links(response)

        # self.parse_js_links(response)
        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.get_js_links)
            # yield scrapy.Request(url, callback=self.parse_js_links)

    # We use selenium to extract script src
    # The instacart case show than many script src are dynamically generated.
    def get_js_links(self, response):

        self.driver.get(response.url)

        elements = self.driver.find_elements_by_xpath('//script')

        with open("../data/" + self.site + "_result.txt", 'a') as f:
            f.write("Page:" + response.url + "\n")
            for element in elements:
                js_src = element.get_attribute("src")

                if js_src != "":
                    f.write(js_src + "\n")
                    print(js_src)

    # Get js links by scrapy. However, since scrapy only handles static page,
    # we could miss some javascript inclusions.
    def parse_js_links(self, response):
        # with open("../data/uber.txt", 'a') as f:
        with open("../data/instacart.txt", 'a') as f:
            f.write("Page:" + response.url + "\n")
            for sel in response.xpath('//script/@src'):
                f.write(sel.extract() + "\n")
                print(sel.extract())

