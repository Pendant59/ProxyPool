import requests
import random
from functions import set_log
from pyquery import PyQuery as pq
from db import RedisClient
from config import HEADERS_LIST


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
		attrs['funnum'] = len(attrs['funclist'])
		# 创建类  不是创建类的实例化对象
		return type.__new__(cls, base, name, attrs)


class GetProxiesData(metaclass=GetProxiesDataMetaClass):
	"""Get proxies from webserver"""
	def __init__(self):
		redis = RedisClient()
		self._proxy = redis.getProxy()

	def get_proxy_xici(self):
		
		url = 'http://www.xicidaili.com/nn/'
		link = requests.Session()
		header = {
			'User-Agent': random.choice(HEADERS_LIST)
		}
		try:
			if not self._proxy:
				res = link.get(url, headers=header, timeout=0.001)
			else:
				res = link.get(url, proxies=self._proxy, headers=header, timeout=4)
			if res.status_code == requests.codes.ok:
				print('success')
		except Exception as e:
			set_log('西刺代理，请求超时', 'proxy')
		finally:
			return None
		
		
		

			

	def get_proxy_goubanjia(self):
		pass
	


if __name__ == '__main__':
	GetProxiesData().get_proxy_xici()