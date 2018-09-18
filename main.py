from db import RedisClient
from config import  GET_PROXY_TIMEOUT,POOL_MIN_NUMBER,POOL_MAX_NUMBER,VALID_PROXY_CYCLE,POOL_MAX_LEN_CYCLE,TEST_API
from getdata import GetProxiesData



class DoCheck():
	""" 检查 """
	def __init__(self):
		self._db = RedisClient()
		pass

		

class DoGrab():
	""" 抓取入库 """
	def __init__(self):
		self._db = RedisClient()
		self._get = GetProxiesData()

	def DoGrab(self):
		''' 抓取 '''
		
		#代理池数量小于100个，开始抓取
		if self._db.getProxyLength < POOL_MAX_NUMBER :
			for index in range(self._get.funcnum):
				proxyList = eval('self._get.{}()'.format(self._get.funclist[index]))
				if proxyList:
				  for proxy in proxyList:
				  	self._db.addProxy(proxy)
				else:
					set_log('Grab proxies').debug('{} is Error'.format(self._get.funclist[index]))
					continue
		else:
			print('ProxyList is full')
		return True



class Main():
	""" The pool controller """

	# 抓取代理
	_grab = DoGrab()
	# 检查代理
	_check = DoCheck()
	
	@staticmethod
	def CheckProxies():
		'''Check whether agents are available'''
		pass
			


	@staticmethod
	def GrabProxies(cycle=POOL_MAX_LEN_CYCLE):
		'''Grabbing proxies'''
		while True:
			_grab.DoGrab()
			time.sleep(cycle)


if __name__ == '__main__':
	Main.GrabProxies()