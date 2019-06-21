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
	'''
	def __new__(cls, base ,name ,attrs):
		'''
		创建类的方法
		'''
		# 类变量 爬虫方法总个数
		attrs['funclist'] = [k for k in attrs.keys() if 'get_proxy_' in k]
		# 类变量 爬虫方法名称集合 从上到下
		attrs['funcnum'] = len(attrs['funclist'])
		return type.__new__(cls, base, name, attrs)


class GetProxiesData(metaclass=GetProxiesDataMetaClass):
	"""
	获取代理IP
	Get proxies from webserver
	"""

	def get_proxy_zdaye(self):
		''' 获取站大爷代理ip'''
		url = 'http://ip.zdaye.com/dayProxy/' + str(time.localtime().tm_year) + '/' + str(time.localtime().tm_mon) + '/1.html'
		db = RedisClient()
		if USE_GET_PROXY:
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None
		html = get_html(url, proxy)
		
		attemp = 1 
		while html is None and attemp <3:
			attemp+=1
			if USE_GET_PROXY:
				proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
			else:
				proxy = None
			html = get_html(url, proxy)
			if html:
				break

		if html:
			proxies = list()
			doc = pq(html)
			urls = [doc('#J_posts_list .thread_theme_type').eq(0).attr('href'), doc('#J_posts_list .thread_theme_type').eq(1).attr('href')]
			if urls:
				for uri in urls:
					time.sleep(random.uniform(1,3))
					ip_url = 'http://ip.zdaye.com' + uri
					html = get_html(ip_url, proxy, False, referer=url)
					if html:
						try:
							doc = pq(html)
							trList = doc('div.cont').text()
							pattern = re.compile(r'(\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3}):(\d{2,5})@HTTP#\[高匿\]', re.M)
							ip_list = pattern.findall(trList)  #[('117.191.11.74', '80'), ('39.137.168.230', '80'), ('117.191.11.73', '80')]
							for i in ip_list:
								ip = i[0]
								port = i[1]
								proxies.append(json.dumps({'http':'http'+'://'+ip+':'+port}))
						except Exception as e:
							# set_log_zh_bytime('analysis_proxy_kuaidaili').debug(e)
							continue
				if proxies:
					return proxies
				return None

	def get_proxy_xici(self):
		'''获取西刺代理ip'''

		url = 'http://www.xicidaili.com/nn/'
		db = RedisClient()
		if USE_GET_PROXY:
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None
		html = get_html(url, proxy)
		
		attemp = 1 
		while html is None and attemp <3:
			attemp+=1
			if USE_GET_PROXY:
				proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
			else:
				proxy = None
			html = get_html(url, proxy, True)
			if html:
				break

		if html:
			proxies = list()
			doc = pq(html)
			try:
				trList = doc('#ip_list tr:gt(0)')
				for x in trList.items():
					delay = x.find('td').eq(6).find("div").attr('title')[0]
					if int(float(delay)) >= 1 :
						continue
					ip = x.find('td').eq(1).text()
					port = x.find('td').eq(2).text()
					agreement = x.find('td').eq(5).text().lower()
					if agreement != 'http': # 只抓取http代理，异步校验只能校验http
						continue
					proxies.append(json.dumps({agreement:agreement+'://'+ip+':'+port}))
				return proxies
			except Exception as e:
				# set_log_zh_bytime('analysis_proxy_xici').debug(e)
				return None
	
	def get_proxy_seofangfa(self):
		
		url = 'http://proxy.seofangfa.com/';
		db = RedisClient()
		proxies = list()

		if USE_GET_PROXY:
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None
	
		html = get_html(url, proxy)

		attemp = 1
		while html is None and attemp < 3:
			attemp+=1
			if USE_GET_PROXY:
				proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
			else:
				proxy = None
			html = get_html(url, proxy, True)
			if html:
				break
		
		if html:
			try:
				doc = pq(html)
				trList = doc('.table tr:gt(0)')
				for x in trList.items():
					delay = x.find('td').eq(2).text()
					if int(float(delay)) >= 1:
						continue
					# 移除国外代理
					location = x.find('td').eq(3).text()
					if '中国' not in location:
						continue
					ip = x.find('td').eq(0).text()
					port = x.find('td').eq(1).text()
					proxies.append(json.dumps({'http':'http'+'://'+ip+':'+port}))
			except Exception as e:
				return None
		return proxies

	def get_proxy_data5u(self):
	
		url = 'http://www.data5u.com/';
		db = RedisClient()
		proxies = list()

		if USE_GET_PROXY:
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None

		html = get_html(url, proxy)

		attemp = 1
		while html is None and attemp < 3:
			attemp+=1
			if USE_GET_PROXY:
				proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
			else:
				proxy = None
			html = get_html(url, proxy, True)
			if html:
				break
		
		if html:
			try:
				doc = pq(html)
				trList = doc('.wlist ul li ul.l2')
				for x in trList.items():
					delay = x.find('span').eq(7).text()
					if int(float(delay[:-1])) >= 2:
						continue
					ip = x.find('span').eq(0).text()
					port = x.find('span').eq(1).text()
					proxies.append(json.dumps({'http':'http'+'://'+ip+':'+port}))
			except Exception as e:
				return None
		return proxies

	def get_proxy_kuaidaili(self):
		'''获取快代理ip'''
		db = RedisClient()
		proxies = list()
		
		if USE_GET_PROXY:
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None

		for page in range(1,3):
			time.sleep(random.uniform(1,3))
			url = 'https://www.kuaidaili.com/free/inha/'+str(page)
			
			html = get_html(url, proxy)
			
			attemp = 1
			while html is None and attemp < 3:
				attemp+=1
				if USE_GET_PROXY:
					proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
				else:
					proxy = None
				html = get_html(url, proxy, True)
				if html:
					break

			if html:
				try:
					doc = pq(html)
					trList = doc('#list table tr:gt(0)')
					for i in trList.items():
						if int(float(i.find('td').eq(5).text()[0])) >= 2:
							continue
						ip = i.find('td').eq(0).text()
						port = i.find('td').eq(1).text()
						agreement = i.find('td').eq(3).text().lower()
						if agreement != 'http': # 只抓取http代理，异步校验只能校验http
							continue
						proxies.append(json.dumps({agreement:agreement+'://'+ip+':'+port}))
				except Exception as e:
					# set_log_zh_bytime('analysis_proxy_kuaidaili').debug(e)
					return None
		return proxies

	def get_proxy_goubanjia(self):
		'''获取goubanjia代理ip'''

		url = 'http://www.goubanjia.com/'
		db = RedisClient()
		
		if USE_GET_PROXY:
			proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
		else:
			proxy = None
		html = get_html(url, proxy)
		
		attemp = 1 
		while html is None and attemp < 3:
			attemp+=1
			if USE_GET_PROXY:
				proxy = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
			else:
				proxy = None
			html = get_html(url, proxy, True)
			if html:
				break

		if html:
			proxies = list()
			doc = pq(html)
			try:
				trList=doc(".table.table-hover tr:gt(0)")
				for i in trList.items():
					ipList =[]
					for v in i.find('.ip').children().items():
						if v.attr('style') != 'display: none;' and v.attr('style') != 'display:none;' and v.text() is not '':
							ipList.append(v.text())
					ip =''.join(ipList[:-1])
					port = ipList[-1]
					agreement = i.find('td').eq(2).text().lower()
					if agreement != 'http': # 只抓取http代理，异步校验只能校验http
						continue
					proxies.append(json.dumps({agreement:agreement+'://'+ip+':'+port}))
				return proxies
			except Exception as e:
				# set_log_zh_bytime('analysis_proxy_goubanjia').debug(e)
				return None


if __name__ == '__main__':
	pass
	# print(GetProxiesData().get_proxy_xici())
	# print(GetProxiesData().get_proxy_kuaidaili())
	# print(GetProxiesData().get_proxy_goubanjia())
	# print(GetProxiesData().get_proxy_seofangfa())
	# print(GetProxiesData().get_proxy_data5u())
	print(GetProxiesData().get_proxy_zdaye())

