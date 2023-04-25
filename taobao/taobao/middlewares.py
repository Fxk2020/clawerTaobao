# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from taobao.settings import JSON_FILE
from taobao.util import create_chrome_driver, add_cookies
from selenium.webdriver.support import expected_conditions as EC

class TaobaoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TaobaoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self):
        # 滑块次数--防止一直需要验证
        self.HK_COUNT = 0

        self.browser = create_chrome_driver(headless=False)
        self.browser.get(' https://www.taobao.com')
        add_cookies(self.browser, JSON_FILE)

    def __del__(self):
        self.browser.quit()

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        self.browser.get(request.url)
        time.sleep(5)
        pageSource = HtmlResponse(url=request.url, body=self.browser.page_source, encoding='utf-8')
        if pageSource.css('#nocaptcha').get() is not None:
            # print("9999999999999999999999999999999999")
            option = Options()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_experimental_option("detach", True)
            js = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
            self.browser.execute_script(js)
            huakuai = WebDriverWait(self.browser, 100).until(
                EC.presence_of_element_located((By.ID, 'nc_1_n1z')))
            # 动作链
            time.sleep(1)
            newaction = ActionChains(driver=self.browser)
            newaction.move_to_element(huakuai)
            newaction.click_and_hold(huakuai)
            # newaction.move_by_offset(300, 0).perform()
            for i in range(100):
                newaction.move_by_offset(3, 0).perform()
                time.sleep(0.003)
            newaction.release()
            self.HK_COUNT = self.HK_COUNT+1
            if self.HK_COUNT == 20:
                time.sleep(1800)
                self.HK_COUNT = 0
            time.sleep(3)

        # print("oooooooooooooooooooooooooo")
        return HtmlResponse(url=request.url, body=self.browser.page_source,
                            request=request, encoding='utf-8')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
