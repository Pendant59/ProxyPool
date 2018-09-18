# Redis数据库的相关配置
# 地址
HOST = 'localhost'
# 端口
PORT = 6379
# 无密码就设置为空
PASSWORD = ''
# 数据库 0-15
DB = 0

# 获取代理的模式 0：取出即删除，1：仅取出
GET_PROXY_TYPE = 0

# 获取代理的header
HEADERS_LIST = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	'Mozilla/5.0 (WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
]


# 获得代理测试时间界限
GET_PROXY_TIMEOUT = 9

# 代理池数量界限
POOL_MIN_NUMBER = 20
POOL_MAX_NUMBER = 100

# 检查周期
VALID_PROXY_CYCLE = 60
POOL_MAX_LEN_CYCLE = 20

# 测试API，用百度来测试
TEST_API='https://www.baidu.com'