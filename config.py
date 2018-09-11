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

# 获得代理测试时间界限
get_proxy_timeout = 9

# 代理池数量界限
POOL_LOWER_THRESHOLD = 20
POOL_UPPER_THRESHOLD = 100

# 检查周期
VALID_CHECK_CYCLE = 60
POOL_LEN_CHECK_CYCLE = 20

# 测试API，用百度来测试
TEST_API='https://www.baidu.com'