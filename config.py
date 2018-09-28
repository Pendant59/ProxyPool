# Redis数据库的相关配置
# 地址
HOST = 'localhost'
# 端口
PORT = 6379
# 无密码就设置为空
PASSWORD = ''
# 数据库 0-15
DB = 0
# Redis bloom filter 去重
BF_DB = 1

# 请求相关配置
# 获取代理的模式 0：取出即删除，1：仅取出
GET_PROXY_TYPE = 0

# 是否使用抓取的代理来请求代理网站，0：不用，1：使用。(若代理池为空，则默认用真实IP) 
USE_GET_PROXY = 1

# 获取代理的header
HEADERS_LIST = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	'Mozilla/5.0 (WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
]

# 测试代理是否可用的超时时间
PROXY_TEST_TIMEOUT = 9

# 请求代理网站的超时时间
PROXY_REQUEST_TIMEOUT = 6

# 代理池相关配置
# 代理池IP数量界限
POOL_MIN_NUMBER = 20
POOL_MAX_NUMBER = 50

# 代理池检查周期
VALID_PROXY_CYCLE = 60
POOL_MAX_LEN_CHECK_CYCLE = 20

# 测试API，用百度来测试
TEST_API='http://www.baidu.com'