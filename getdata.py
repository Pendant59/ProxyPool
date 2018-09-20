import random
import json
import re
from config import USE_GET_PROXY
from functions import *
from pyquery import PyQuery as pq
from db import RedisClient



class GetProxiesDataMetaClass(type):
	'''
	元类
	可以控制类的创建，动态的更改类或者实例化对象的的属性或者方法
	一般情况下不需要使用元类，当前元类实现的功能完全可以放到爬虫类的__init__中实现
	'''
	def __new__(cls, base ,name ,attrs):
		'''
		创建类的方法
		cls: 将要创建的类,类似于self,但是self指向的是instance(实例),而这里cls指向的是class。
		name: 类的名字,也就是我们通常用类名.__name__获取的。
		bases: 基类通常是(object,) 可以为空。
		attrs: 属性的dict,dict的内容可以是变量(类属性),也可以是函数(类方法)。
		'''
		# 类变量 爬虫方法总个数
		attrs['funclist'] = [k for k in attrs.keys() if 'get_proxy_' in k]
		# 类变量 爬虫方法名称集合
		attrs['funcnum'] = len(attrs['funclist'])
		# 创建类  不是创建类的实例化对象
		return type.__new__(cls, base, name, attrs)


class GetProxiesData(metaclass=GetProxiesDataMetaClass):
	"""Get proxies from webserver"""

	def get_proxy_xici(self):
		'''获取西刺代理ip'''

		url = 'http://www.xicidaili.com/nn/'
		# url = 'http://www.google.com'
		db = RedisClient()
		# 是否启用抓取的代理来发起请求
		if USE_GET_PROXY:
			# 获取一条代理
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None
		html = get_html(url, proxy)
		# 失败重试
		attemp = 1 
		while html is None and attemp <3:
			attemp+=1
			# 是否启用抓取的代理来发起请求
			if USE_GET_PROXY:
				# 获取一条代理
				proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
			else:
				proxy = None
			html = get_html(url, proxy, True)
			if html:
				break
		# 解析 Html 结构
		if html:
			# 返回列表
			proxies = list()
			doc = pq(html)
			try:
				trList = doc('#ip_list tr:gt(0)')
				for x in trList.items():
					delay = x.find('td').eq(6).find("div").attr('title')[0]
					if int(delay) > 0 :
						continue
					ip = x.find('td').eq(1).text()
					port = x.find('td').eq(2).text()
					agreement = x.find('td').eq(5).text().lower()
					if agreement != 'http': # 只抓取http代理，异步校验只能校验http
						continue
					proxies.append(json.dumps({agreement:agreement+'://'+ip+':'+port}))
				# print(proxies)
				return proxies
			except Exception as e:
				set_log_zh_bytime_bytime('analysis_proxy_xici').debug(e)
				return None


	def get_proxy_goubanjia(self):
		'''获取goubanjia代理ip'''

		url = 'http://www.goubanjia.com/'
		db = RedisClient()
		# 是否启用抓取的代理来发起请求
		if USE_GET_PROXY:
			# 获取一条代理
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None
		html = get_html(url, proxy)
		
		# 失败重试
		attemp = 1 
		while html is None and attemp < 3:
			attemp+=1
			# 是否启用抓取的代理来发起请求
			if USE_GET_PROXY:
				# 获取一条代理
				proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
			else:
				proxy = None
			html = get_html(url, proxy, True)
			if html:
				break
		# 解析 Html 结构
		if html:
			# 返回列表
			proxies = list()
			doc = pq(html)
			try:
				trList=doc(".table.table-hover tr:gt(0)")
				# 全部tr
				for i in trList.items():
					# 存放ip数据
					ipList =[]
					# 包含ip
					for v in i.find('.ip').children().items():
						if v.attr('style') != 'display: none;' and v.attr('style') != 'display:none;' and v.text() is not '':
							ipList.append(v.text())
					ip =''.join(ipList[:-1])
					port = ipList[-1]
					agreement = i.find('td').eq(2).text().lower()
					if agreement != 'http': # 只抓取http代理，异步校验只能校验http
						continue
					proxies.append(json.dumps({agreement:agreement+'://'+ip+':'+port}))
				# print(proxies)
				return proxies
			except Exception as e:
				set_log_zh_bytime('analysis_proxy_goubanjia').debug(e)
				return None

	def get_proxy_kuaidaili(self):
		'''获取快代理ip'''
		db = RedisClient()
		# 返回列表
		proxies = list()
		# 是否启用抓取的代理来发起请求
		if USE_GET_PROXY:
			# 获取一条代理
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None

		#抓取三页
		for page in range(1,4):
			# 首页限制 加2秒休眠
			time.sleep(random.uniform(1,3))
			url = 'https://www.kuaidaili.com/free/inha/'+str(page)
			
			html = get_html(url, proxy)
			# 失败重试
			attemp = 1
			while html is None and attemp < 3:
				attemp+=1
				# 是否启用抓取的代理来发起请求
				if USE_GET_PROXY:
					# 获取一条代理
					proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
				else:
					proxy = None
				html = get_html(url, proxy, True)
				if html:
					break
			# 解析 Html 结构
			if html:
				try:
					doc = pq(html)
					trList = doc('#list table tr:gt(0)')
					for i in trList.items():
						if int(i.find('td').eq(5).text()[0]) > 2:
							continue
						ip = i.find('td').eq(0).text()
						port = i.find('td').eq(1).text()
						agreement = i.find('td').eq(3).text().lower()
						if agreement != 'http': # 只抓取http代理，异步校验只能校验http
							continue
						proxies.append(json.dumps({agreement:agreement+'://'+ip+':'+port}))
				except Exception as e:
					set_log_zh_bytime('analysis_proxy_kuaidaili').debug(e)
		# print(proxies)
		return proxies
	
	def get_proxy_66(self):
		
		url = {
		'1': 'http://www.66ip.cn/nmtq.php?getnum=20&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=%B1%B1%BE%A9&area=1&proxytype=0&api=66ip',
		'2': 'http://www.66ip.cn/nmtq.php?getnum=20&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=%C9%CF%BA%A3&area=1&proxytype=0&api=66ip'
		}
		db = RedisClient()
		# 返回列表
		proxies = list()
		# 是否启用抓取的代理来发起请求
		if USE_GET_PROXY:
			# 获取一条代理
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None
		for index in ['1','2']:
			html = get_html(url[index], proxy)
			# 失败重试
			attemp = 1
			while html is None and attemp < 3:
				attemp+=1
				# 是否启用抓取的代理来发起请求
				if USE_GET_PROXY:
					# 获取一条代理
					proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
				else:
					proxy = None
				html = get_html(url[index], proxy, True)
				if html:
					break
			# 解析 Html 结构
			if html:
				try:
					doc = pq(html)
					proxiesList = re.findall(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{2,4})', doc.text())
					for ipstr in proxiesList:
						proxies.append(json.dumps({'http':'http'+'://'+ ipstr}))
				except Exception as e:
					set_log_zh_bytime('analysis_proxy_66').debug(e)
					return None
		# print(proxies)
		return proxies


if __name__ == '__main__':
	pass
	# print(GetProxiesData().get_proxy_kuaidaili())
	# print(GetProxiesData().get_proxy_goubanjia())
	# print(GetProxiesData().get_proxy_66())

