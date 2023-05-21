## 使用scrapy框架去爬取淘宝数据

学习了信息检索这么课最大的感悟就是获取数据的能力增加了。之前想获取什么数据集第一想法是去互联网上查询，现在就是想能不能自己爬取下来用。

系统学习了爬虫的相关知识，掌握了scrapy框架的使用。并且学习了selenium自动化操作框架。

实战以淘宝为例，爬取淘宝的商品信息：

![image-20230521175138237](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230521175138237.png)

最终获得了

- 1093条关键词下180多万条商品信息。（本来想爬取2000条关键词的但是时间来不及了）
- ![image-20230521195310009](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230521195310009.png)
- ![image-20230521195322406](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230521195322406.png)
- ![image-20230521195259653](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230521195259653.png)

### 1 使用selenium驱动谷歌浏览器

需要下载对应版本的驱动

```
bro = webdriver.Chrome(executable_path=WEBDRIVER_PATH)
option = Options()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option("detach", True)
script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
bro.execute_script(script)
```

WEBDRIVER_PATH就是驱动的路径

### 2 模拟用户登录获取cookies

![image-20230521174901004](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230521174901004.png)

```
Demo20.py
```

- 使用selenium模拟人填入用户名，密码，点击登录按钮
- 淘宝存在滑块验证--验证一次（**重点在于滑块在一个frame中，需要转换页面，否则一直找不到那个元素**）

- 恶心的是淘宝滑块通过点击登录按钮之后，它还会让你在滑块验证一次。（再次调用SwitchFrame方法就可以了）
- 将登录之后获取的cookie放到taobao.json中

### 3 使用scrapy解析页面

![image-20230521174623420](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230521174623420.png)

#### 3.1 middlewares中使用下载中间件--解决爬的次数多了需要滑块验证

```
DownloaderMiddleware在下载前处理滑块问题
```

```
__init__中初始化浏览器，加入cookie信息
```

```
process_request如果有滑块验证模拟人工滑块解封，并且返回给爬虫htmlresponse信息
```

```
pageSource = HtmlResponse(url=request.url, body=self.browser.page_source, encoding='utf-8')该方法用于返回网页检查中的源代码--用于捕捉动态加载的网页
```

主要用于解决用户多次访问需要验证和将网页动态内容捕捉给爬虫的问题

#### 3.2 taobao爬虫解析下载中间件返回的htmlresponse

```
keywords = read_keywords(KEY_WORDS_FILE)输入关键字的文件
```

格式如下

![image-20230421171611980](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230421171611980.png)



```
start_requests中进行url申请
```

```
parse(self, response)对网页源代码进行分析，这里有个问题就是淘宝有两套样式表（我目前爬到的），所以要分两种写（真的难受），用到css解析
```

![image-20230421193624685](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230421193624685.png)

#### 3.3 Itme中的字段--和数据库相对应

```
class TaobaoItem(scrapy.Item):
    title = scrapy.Field()  # 商品名
    prize = scrapy.Field()  # 商品价格
    content = scrapy.Field()  # 商品详情
    people_buy = scrapy.Field()  # 商品购买人数
    shop_name = scrapy.Field()  # 店铺名称
    shop_url = scrapy.Field()  # 店铺url
    item_type = scrapy.Field()  # 商品种类
```

![image-20230510102207873](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230510102207873.png)

#### 3.4 popelines将itmes输出到数据库中

```
__init__连接到数据库
```

```
process_item爬到数据后调用数据库进行存储
```

```
close_spider关闭爬虫时，将剩余数据写入数据库，关闭数据库
```

#### 3.5 setting中配置一系列数据

![image-20230421193918148](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230421193918148.png)

keywords中保存了需要爬取的一些列关键字

![image-20230421193939900](https://oss-img-fxk.oss-cn-beijing.aliyuncs.com/markdown/image-20230421193939900.png)

#### 3.6 util工具类中的方法

```
create_chrome_driver创建谷歌的浏览器驱动
```

```
add_cookies读取json中的cookie信息并加入到浏览器中
```

```
re_font使用正则表达式使字符串只剩下汉字
```

```
read_keywords读取关键字并返回关键字列表
```

### 4.用到的类包

- requestments.txt中包含项目中所用到的类包以及版本

- Python 3.11.0

- ```
  DB_HOST = ""
  DB_USER = ""
  DB_PASSWORD = ""
  DB_DATABASE = ""
  DB_CHARSET = "utf8"
  
  WEBDRIVER_PATH = ''
  # Crawl responsibly by identifying yourself (and your website) on the user-agent
  #USER_AGENT = "taobao (+http://www.yourdomain.com)"
  
  USER_NAME = ""
  USER_PASSWORD = ""
  填上自己的信息
  ```

### 5.源代码

源代码已经上传到github，地址：https://github.com/Fxk2020/clawerTaobao。

### 6.对爬取的数据进行分析

放到了自己的github上：https://github.com/Fxk2020/taobaoPythonAnalysis
