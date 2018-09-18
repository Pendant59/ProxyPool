from db import RedisClient
from config import  GET_PROXY_TIMEOUT,POOL_MIN_NUMBER,POOL_MAX_NUMBER,VALID_PROXY_CYCLE,POOL_MAX_LEN_CYCLE,TEST_API
from getdata import GetProxiesData
import time



class DoCheck():
	""" 检查 """
	def __init__(self):
		self._db = RedisClient()

	def DoCheck(self):
		''' 校验代理 '''
		waitForCheckList = self._db.validateProxiesList()
		waitForCheckList = [proxy.decode('utf-8') for proxy in waitForCheckList ]
		print(waitForCheckList)

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
	def GrabProxies():
		'''Grabbing proxies'''
		while True:
			Main._grab.DoGrab()
			time.sleep(POOL_MAX_LEN_CYCLE)


if __name__ == '__main__':
	# Main.GrabProxies()
	# DoCheck().DoCheck()