## Python爬虫入门（一）

### 技术路线：requests + bs4 + re

#### 1.requests

- requests库负责向指定URL下载和传送数据，拉取指定网页的HTML内容，在python中，典型的代码框架是：

  `安装： pip3 install requests`

  ```
  import requests
  def getHTMLText(url):
  	try:
  		r = requests.get(url)
  		r.raise_for_status()
  		r.encoding = r.apparent_encoding
  		return r.text
  	except:
  		return "Exception generated"
  ```

  其中，get函数返回Response对象，该对象有以下几个常用**属性**：

  |       属性        |               描述               |
  | :---------------: | :------------------------------: |
  |       text        |  返回网页的HTML格式，string类型  |
  |     contents      |       返回网页的二进制形式       |
  |     encoding      | 从网页头部判断而来的网页编码方式 |
  | apparent_encoding |    根据网页内容推断的编码方式    |
  |    status_code    |            HTTP状态码            |
  |      request      |   向网站请求数据的HTTP请求报文   |

  

- 下面介绍requests的7个**库方法**

  |                    方法                     | 描述                                                         |
  | :-----------------------------------------: | :----------------------------------------------------------- |
  |                  request()                  | requests库的基础方法，以下几个方法都是基于该方法封装而来，使用较少 |
  |      get(url, params= None, **kwargs)       | 爬虫时使用最多的方法, params以**字典**形式给出               |
  |             head(url, **kwargs)             | 获取网页头部，适合爬大量数据前获取网页的概要信息             |
  | \*post(url, data=None, json=None, **kwargs) | 使用post方法向网页上传数据                                   |
  |       \*put(url, data=None, **kwargs)       | 更新全部字段，覆盖原位置资源                                 |
  |      \*patch(url, data=None, **kwargs)      | 更新局部字段，不会破坏原位置数据                             |
  |           \*delete(url, **kwargs)           | 删除网页资源                                                 |

  > **\***: 爬虫通常是从网页下行拉取数据，加上网站一般不允许用户操作服务器上的资源，所以这几个方法我们很少用到

  大家或许留意到，这几个方法不就是HTTP报文中的方法字段值吗？没错这几个方法就是基于HTTP协议中数据交换方法定义的，所以我们顺便简要复习一下HTTP的两种报文：请求报文和响应报文。

  ​	HTTP报文是**面向文本**的，因此报文中的每个字段都是ASCII码串，报文都由三个部分组成：***开始行***、***首部行***、***实体主体***。二者的区别只是**开始行**不同。

  | 报文类型 |           开始行           |
  | :------: | :------------------------: |
  | 请求报文 |   \|**方法**\| URL\|版本   |
  | 响应报文 | \|版本\|**状态码**\|短语\| |

  其中请求报文的方法字段值就包含了requests的几种库方法。

  响应报文的状态码可以通过 **r.status_code**属性得到，200表示正确数据

  #### 2.Robots协议

  - 作用：向全网宣告本网站哪些内容不能爬取

  - 描述文件位置：网站根目录下的robots.txt

  - 遵守方式：建议性，非强制性，频率适度的爬虫可以不遵守robots协议（手动滑稽

    下面是淘宝的robots.txt:

    ![](/Users/mahonghui/Downloads/image.png)

  #### 3. BeautifulSoup4 (bs4)

  解析HTML，XML，YAML利器

  `安装： pip3 install BeautifulSoup4`

  ```
  from bs4 import BeautifulSoup4 as bs4 # 虽然安装的是BeautifulSoup4，但这里from依然用bs4
  soup = bs4(r.text, 'html.parser')) # 解析网页用html.parser, xml同理
  ```

可以把解析后的soup理解为一棵标签树，类似于DOM，我们后面可以使用各种方法对这棵树进行遍历，得到目标数据。

1. BS类属性

   | 属性            | 描述                                         |
   | --------------- | -------------------------------------------- |
   | tag             | 标识该节点为标签节点                         |
   | name            | 该标签的name，'<p>'.name 是 'p'              |
   | attrs           | 字典类型，存储标签属性和对应值的键值对       |
   | navigablestring | 非属性字符串，<tag>.string获取标签包围的内容 |
   | comment         | 注释部分                                     |

   

2.标签树的下行遍历

​	.contents: 当前<tag>的子节点列表

​	.children: 子节点的迭代类型

​	.descendants: 所有子孙节点的迭代类型

3. 上行遍历

   \.parent: 当前<tag>的直接父节点

   \.parents: 当前<tag>的所有父辈，可迭代类型

   4. 层级遍历

      ​	next_sibling previous_sibling

   可迭代：next_siblings previous_siblings 

   

   5. 解析网页时，最常用的莫过于 <font color='red'>find_all(name, attrs, recursive, string, \*\*kwargs</font>

      参数解释：

       - name：要检索的标签名称

       - attrs：检索具有特定属性值的标签，以字典形式给出

       - recursive：False只在下一级子节点中检索

       - string：检索包含特定内容的标签， 匹配对象是前面说过的navigablestring

         > 注：find() 函数与find_all(),用法相同，只不过前者返回第一个匹配的标签，后者返回所有匹配结果列表

   

#### 4. re 正则表达式库



