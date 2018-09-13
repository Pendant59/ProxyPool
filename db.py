import redis
import random
from functions import set_log
from config import *
try:
	from retrying import retry
except Exception as e:
	print('retrying module is not avaliable.')


class RedisClient():
	'''
	连接Redis 
	Connect to Redis
	'''
	def __init__(self, HOST=HOST, PORT=PORT, PASSWORD=PASSWORD, DB=DB):
		try:
			if PASSWORD:
				pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB)
			else:
				pool = redis.ConnectionPool(host=HOST, password=PASSWORD,port=PORT, db=DB)
			self._db = redis.Redis(connection_pool=pool)
		except Exception as e:
			set_log(e, 'error', '__init__')
			print('Redis Content is error. Please check the ErrorLog.')
			exit()

	@retry(stop_max_attempt_number=5, wait_fixed=4000)
	def getOnceProxy(self):
		'''
		获取一次性代理 - 用过删除
		Get a disposable proxy
		'''
		try:
			proxy = self._db.rpop('proxy').decode('utf-8')
			return proxy
		except Exception as e:
			set_log(e, 'error', 'getOnceProxy')
			print('Get a disposable proxy is error. Please check the ErrorLog.')
			exit()

	@retry(stop_max_attempt_number=5, wait_fixed=4000)
	def getProxy(self):
		'''
		获取代理 - 用过不删除
		Get proxy - used without deletion
		'''
		if self.getProxyLength == 0:
			return None

		try:
			proxy = self._db.lindex('proxy', random.randint(0, self.getProxyLength-1)).decode('utf-8')
			return proxy
		except Exception as e:
			set_log(e, 'error', 'getProxy')
			print('Get proxy - used without deletion is error. Please check the ErrorLog.')
			exit()

	def validateProxiesList(self):
		'''
		获取需要校验的代理列表
		Get the list of proxys that need to be checked
		'''
		if self.getProxyLength == 0:
			return None

		proxies_list = self._db.lrange('proxy', 0, self.getProxyLength // 2)
		return proxies_list

	def addProxy(self,value):
		'''
		添加代理
		add proxy
		'''
		if value:
			self._db.rpush('proxy', value)

	@property
	def getProxyLength(self):
		'''
		获取代理队列长度
		Get proxy queue length
		'''
		return self._db.llen('proxy')
	
	def flushDb(self):
		'''
		清空当前选择的数据库
		flush db
		'''
		self._db.flushdb()


if __name__ == '__main__':
    redis = RedisClient(PORT=6379)
    if GET_PROXY_TYPE:
    	proxy = redis.getProxy()
    else:
    	proxy = redis.getOnceProxy()
    print(proxy)


			
		
