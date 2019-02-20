# coding: utf-8

import requests
from bs4 import BeautifulSoup

def getHtmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parse(text):
    selector = BeautifulSoup(text, "html.parser")
    p = selector.find('p', class_="query-hd").get_text()
    return p

def main():
    url_template = "http://m.ip138.com/youbian/youbian.asp?zip={zipcode}&action=zip2area"
    zipcode = int(input("请输入要查询的邮编：")[:-1])
    resp = parse(getHtmlText(url_template.format(zipcode=zipcode)))
    print(resp)


if __name__ == "__main__":
    main()


