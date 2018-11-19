import time
import asyncio
import aiohttp
import json
from db import RedisClient
from getdata import GetProxiesData
from functions import set_log_zh_bytime
from config import *
from bloomfilter import BloomFilter


class DoCheck():
	""" 检查 """
	def __init__(self):
		self._db = RedisClient()
		self._bf = BloomFilter()
		
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
			pass
		

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
								if USE_BLOOMFILTER:
									if not self._bf.isContains(json.dumps(proxy)):
										self._db.addProxy(json.dumps(proxy))
									if self._db.getProxyLength > POOL_MIN_NUMBER:
										self._bf.insert(json.dumps(proxy))
								else:
									self._db.addProxy(json.dumps(proxy))
				except Exception as e:
					pass
		except Exception as s:
			pass
		

class DoGrab():
	""" 抓取入库 """
	def __init__(self):
		self._db = RedisClient()
		self._get = GetProxiesData()
		self._check = DoCheck()

	def DoGrab(self):
		''' 抓取 '''
		for index in range(self._get.funcnum):
			proxyList = eval('self._get.{}()'.format(self._get.funclist[index]))
			if proxyList:
				self._check.DoCheck(proxyList)

class Main():
	""" 主控制器类 """

	# 抓取代理
	_grab = DoGrab()
	# 检查代理
	_check = DoCheck()
	# redis
	_db = RedisClient()
	# log
	# _log = {
	# 		'Check_Cycle': set_log_zh_bytime('Check_Cycle'),
	# 		'Grab_Cycle': set_log_zh_bytime('Grab_Cycle')
	# 		}

	@staticmethod
	def CheckProxies():
		'''Check whether agents are available'''
		while True:
			Main._db._db.set('Check', str(int(time.time())))
			if Main._db.getProxyLength > POOL_MIN_NUMBER:
				waitForCheckList = Main._db.validateProxiesList()
				if waitForCheckList:
					Main._check.DoCheck(waitForCheckList)
			else:
				pass
				if USE_BLOOMFILTER:
					Main._check._bf.resetBloomFilter()
			time.sleep(VALID_PROXY_CYCLE)

	@staticmethod
	def GrabProxies():
		'''Grabbing proxies'''
		i = 0
		while True:
			Main._db._db.set('Get', str(int(time.time())))
			if Main._db.getProxyLength < POOL_MAX_NUMBER :
				Main._grab.DoGrab()
			else:
				if i > 5:
					Main._db.delProxys()
					i = 0
				else:
					i += 1
			time.sleep(POOL_MAX_LEN_CHECK_CYCLE)

			
			

if __name__ == '__main__':
	pass
	# Main.GrabProxies()
	# Main.CheckProxies()
