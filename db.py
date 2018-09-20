import redis
import random
import json
from functions import set_log_zh_bytime
from config import HOST,PORT,PASSWORD,DB,GET_PROXY_TYPE


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
			set_log_zh_bytime('db').debug('Redis Content is error. Please check the ErrorLog.')
			exit()

	
	def getOnceProxy(self):
		'''
		获取一次性代理 - 用过删除
		Get a disposable proxy
		'''
		# 当前没有代理
		if self.getProxyLength == 0:
			return None

		try:
			proxy = self._db.rpop('proxy').decode('utf-8')
			return json.loads(proxy)
		except Exception as e:
			set_log_zh_bytime('db').debug('Get a disposable proxy is error {}'.format(e))
			exit()

	def getProxy(self):
		'''
		获取代理 - 用过不删除
		Get proxy - used without deletion
		'''
		# 当前没有代理
		if self.getProxyLength == 0:
			return None

		try:
			proxy = self._db.lindex('proxy', random.randint(0, self.getProxyLength-1)).decode('utf-8')
			return json.loads(proxy)
		except Exception as e:
			set_log_zh_bytime('db').debug('Get proxy whitch is used without deletion is error {}'.format(e))
			exit()

	def validateProxiesList(self):
		'''
		获取需要校验的代理列表
		Get the list of proxys that need to be checked
		'''
		# 获取需要校验的ip列表
		proxies_list = self._db.lrange('proxy', 0, self.getProxyLength // 2)
		# 重置队列长度
		self._db.ltrim('proxy',self.getProxyLength // 2 + 1, -1)
		
		return proxies_list

	def addProxy(self,value):
		'''
		添加代理
		add proxy
		'''
		if value:
			self._db.rpush('proxy', value)
		return True

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
    print(proxy)   # getOnceProxy()


			
		
