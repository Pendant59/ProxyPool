from db import RedisClient
from config import  GET_PROXY_TIMEOUT,POOL_MIN_NUMBER,POOL_MAX_NUMBER,GET_PROXY_TIMEOUT,VALID_PROXY_CYCLE,POOL_MAX_LEN_CHECK_CYCLE,TEST_API
from getdata import GetProxiesData
import time
import asyncio
import aiohttp
from functions import set_log_zh_bytime
import json



class DoCheck():
	""" 检查 """
	def __init__(self):
		self._db = RedisClient()

	def DoCheck(self, proxyList=''):
		''' 校验代理 '''
		if proxyList: # 抓取校验
			waitForCheckList = proxyList
		else:	# 定时检测
			waitForCheckList = self._db.validateProxiesList()
		try:
			loop = asyncio.get_event_loop()
			tasks = [self.AsyncCheck(proxy.decode('utf-8')) if isinstance(proxy,bytes) else self.AsyncCheck(proxy) for proxy in waitForCheckList ]
			loop.run_until_complete(asyncio.wait(tasks))
		except Exception as e:
			set_log_zh_bytime('AsyncCheck').debug(e)
		

	async def AsyncCheck(self,proxy):
		''' 异步校验代理 '''
		try:
			async with aiohttp.ClientSession() as session:
				try:
					proxy = json.loads(proxy)
					if 'http' in proxy:
						proxyStr = proxy['http']
						async with session.get(TEST_API, proxy=proxyStr, timeout=GET_PROXY_TIMEOUT) as response:
							if response.status == 200:
								self._db.addProxy(json.dumps(proxy))
								print('insert', proxyStr, '当前队列长度 :', self._db.getProxyLength)
				# except (asyncio.TimeoutError,aiohttp.client_exceptions.ServerDisconnectedError, aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientHttpProxyError) as e:
				except Exception as e:
					print('useless proxy', proxyStr)
		except Exception as s:
			print('aiohttp error',s)
		

class DoGrab():
	""" 抓取入库 """
	def __init__(self):
		self._db = RedisClient()
		self._get = GetProxiesData()
		self._check = DoCheck()

	def DoGrab(self):
		''' 抓取 '''

		#代理池数量小于100个，开始抓取
		if self._db.getProxyLength < POOL_MAX_NUMBER :
			for index in range(self._get.funcnum):
				print('GET Proxies from : ',self._get.funclist[index])
				proxyList = eval('self._get.{}()'.format(self._get.funclist[index]))
				if proxyList:
					self._check.DoCheck(proxyList)
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
			time.sleep(POOL_MAX_LEN_CHECK_CYCLE)


if __name__ == '__main__':
	Main.GrabProxies()
	# DoCheck().DoCheck()