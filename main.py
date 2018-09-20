import time
import asyncio
import aiohttp
import json
from db import RedisClient
from getdata import GetProxiesData
from functions import set_log_zh_bytime
from config import  PROXY_TEST_TIMEOUT,POOL_MIN_NUMBER,POOL_MAX_NUMBER,VALID_PROXY_CYCLE,POOL_MAX_LEN_CHECK_CYCLE,TEST_API



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
						async with session.get(TEST_API, proxy=proxyStr, timeout=PROXY_TEST_TIMEOUT) as response:
							if response.status == 200:
								self._db.addProxy(json.dumps(proxy))
								# print('insert', proxyStr, '当前队列长度 :', self._db.getProxyLength)
				# except (asyncio.TimeoutError,aiohttp.client_exceptions.ServerDisconnectedError, aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientHttpProxyError) as e:
				except Exception as e:
					pass
					# print('Useless Proxy ', proxyStr)
		except Exception as s:
			pass
			# print('Aiohttp Error',s)
		

class DoGrab():
	""" 抓取入库 """
	def __init__(self):
		self._db = RedisClient()
		self._get = GetProxiesData()
		self._check = DoCheck()

	def DoGrab(self):
		''' 抓取 '''
		for index in range(self._get.funcnum):
			# print('Get Proxies From Func -> : ',self._get.funclist[index])
			proxyList = eval('self._get.{}()'.format(self._get.funclist[index]))
			if proxyList:
				self._check.DoCheck(proxyList)
	"""
	def TestDoGrab(self):
		'''测试抓取，无校验 '''
		
		# 代理池数量小于POOL_MAX_NUMBER，开始抓取
		if self._db.getProxyLength < POOL_MAX_NUMBER :
			for index in range(self._get.funcnum):
				proxyList = eval('self._get.{}()'.format(self._get.funclist[index]))
				if proxyList:
				  for proxy in proxyList:
				  	self._db.addProxy(proxy)
				  	# print('add ', proxy)
				else:
					set_log_zh_bytime('Grab proxies').debug('{} is Error'.format(self._get.funclist[index]))
					continue
		else:
			pass
			
		return True
	"""

class Main():
	""" The pool controller """

	# 抓取代理
	_grab = DoGrab()
	# 检查代理
	_check = DoCheck()
	# redis
	_db = RedisClient()


	@staticmethod
	def CheckProxies():
		'''Check whether agents are available'''
		while True:
			set_log_zh_bytime('Check_Cycle').debug('开始批量校验,当前队列长度： {}'.format(Main._db.getProxyLength))
			if Main._db.getProxyLength > POOL_MIN_NUMBER:
				# print('Check whether agents are available...')
				waitForCheckList = Main._db.validateProxiesList()
				set_log_zh_bytime('Check_Cycle').debug('批量校验取值后的队列长度： {}'.format(Main._db.getProxyLength))
				if waitForCheckList:
					Main._check.DoCheck(waitForCheckList)
			else:
				pass
				set_log_zh_bytime('Check_Cycle').debug('代理数量较少,取消检测,等待填充....')
				# print("The proxy queue isn't long enough. Please wait for filling...")
			time.sleep(VALID_PROXY_CYCLE)




	@staticmethod
	def GrabProxies():
		'''Grabbing proxies'''
		while True:
			# print('Grabbing proxies...')
			# 代理池数量小于POOL_MAX_NUMBER，开始抓取
			if Main._db.getProxyLength < POOL_MAX_NUMBER :
				set_log_zh_bytime('Grab_Cycle').debug('开始抓取 当前队列长度： {}'.format(Main._db.getProxyLength))
				Main._grab.DoGrab()
			else:
				set_log_zh_bytime('Grab_Cycle').debug('代理池已满,无需抓取,等待空位....')
			time.sleep(POOL_MAX_LEN_CHECK_CYCLE)

			
			

if __name__ == '__main__':
	pass
	# Main.GrabProxies()
	# Main.CheckProxies()
	# DoGrab().TestDoGrab()