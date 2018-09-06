# codingL utf-8

import urllib.request
import http.cookiejar


def storeCookie(url, filename):

	cookie = http.cookiejar.MozillaCookieJar(filename)

	handler = urllib.request.HTTPCookieProcessor(cookie)

	opener = urllib.request.build_opener(handler)
	response = opener.open(url)
	cookie.save(ignore_discard=True, ignore_expires = True)

# cookie = http.cookiejar.MozillaCookieJar(filename)
# /*创建Cookie处理器*/
# handler = urllib.request.HTTPCookieProcessor(cookie)
# /*构建opener*/
# opener = urllib.request.build_opener(handler)
# response = opener.open("https://www.douban.com/")
# cookie.save(ignore_discard=True, ignore_expires=True)