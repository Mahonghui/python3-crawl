## wrap push-over package
## input: 
		# str message(required)： 要发送的消息
		# str title(optional): 消息标题，默认APP名称
		# str url(optional): 文本中的URL
		# str url_title(optional): URL标题，默认使用链接

import requests


class PushIt():

	def __init__(self):
	
		self.api = 'https://api.pushover.net/1/messages.json?user={user}&token={token}&message={msg}&title={title}&url={u}&url_title={ut}'
		self.user = 'un7nwysd2ma32rvjpwzvmsbzck2iqv'
		self.token = 'aktaskhj8ygqgwd4tkwjsxwa6cgkyd'

	def push(self, message, title='', url='', url_title=''):

		full_url = self.api.format(
				user=self.user, 
				token=self.token, 
				msg=message, 
				title=title, 
				u=url, 
				ut=url_title
				)
		requests.post(full_url)


