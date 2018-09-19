import time
import logging
import logging.handlers
from config import HEADERS_LIST,GET_PROXY_TYPE,PROXY_REQUEST_TIMEOUT
import random
import requests
import urllib3
urllib3.disable_warnings()

def get_html(url,proxy='',retry=False,**options):
    '''
    获取url的html代码
    url: 目标url
    proxy: 代理ip
    retry: 是否是重试请求
    options: header头其他参数
    '''
   
    header = {
        'User-Agent': random.choice(HEADERS_LIST),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    headers = dict(header, **options)
 
    link = requests.Session()
    link.headers["Connection"] = 'close'

    try:
        if proxy:
            r = link.get(url, headers=headers, proxies=proxy, timeout=PROXY_REQUEST_TIMEOUT, verify=False)
        else:
            r = link.get(url, headers=headers, timeout=PROXY_REQUEST_TIMEOUT, verify=False)
        print('Get Proxies From Url -> ', url, r.status_code)
        if r.status_code == requests.codes.ok:
            return r.text
    except Exception as e:
        # 重试还失败则记录日志
        if retry:
            set_log_zh_bytime('request_proxy').debug('{}\r\n{}'.format(url,e))
  


def set_log(logname='', openmethod='a+'):
    ''' 
    简单记录英文日志
    logname: 日志文件标识
    openmethod: 日志读写方式
    '''
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'.log'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%d-%m %p"
    # 内容格式
    contentFormat = '\r\n [ %(asctime)s ] -%(pathname)s- [ line:%(lineno)d ] -- %(levelname)s -- '
    contentFormat += '\r\n=|=\r\n %(message)s \r\n=|='
    # 一次性基础配置
    logging.basicConfig(level=logging.DEBUG,  
                    format= contentFormat,
                    datefmt = dateFormat,
                    filename= fileName,  
                    filemode=openmethod)
    return logging


def set_log_zh(logname='', openmethod='a+'):
    '''
    记录中文日志
    logname: 日志文件标识
    openmethod: 日志读写方式
    **_**_**
    声明一个 Logger 对象，
    然后指定Logger对象对应的 Handler 为 FileHandler 对象，
    然后 Handler 对象还单独指定了 Formatter 对象单独配置输出格式，
    最后给 Logger 对象添加对应的 Handler 
    然后 即可输出日志
    Formatter->Handler->Logger->Logger.debug()
    '''

    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'-zh.log'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%d-%m %p"
    # 内容格式
    contentFormat = '\r\n [ %(asctime)s ] -%(pathname)s- [ line:%(lineno)d ] -- %(levelname)s -- '
    contentFormat += '\r\n=|=\r\n %(message)s \r\n=|='

    # 1.创建 logger对象(记录器)：负责产生日志
    logger = logging.getLogger('zh') #获得一个logger对象，默认是root
    
    # 2.设置日志级别
    logger.setLevel(logging.DEBUG)

    # 3.创建 Formatter对象(格式构造器)：指定日志结果的输出格式和时间格式
    formmater = logging.Formatter(contentFormat, datefmt=dateFormat)
    
    # 4.创建 Handler对象(处理器)：接收logger传来的日志，然后控制输出
    handler = logging.FileHandler(fileName,openmethod,encoding='utf-8') 
    
    # 5.为Handler对象绑定Formatter对象，即规定了Handler对象输出日志的格式
    handler.setFormatter(formmater)
    
    # 6.判断handler是否已挂载到Logger对象上，已挂载则直接输出日志，未挂载则先挂载再输出日志

    if not logger.hasHandlers():
        logger.addHandler(handler)
    
    # 7.返回记录器对象
    return logger
    
    


def set_log_zh_bytime(logname=''):
    '''
    按时间分割记录中文日志
    logname: 日志文件标识
    **_**_**
    声明一个 Logger 对象，
    然后指定Logger对象对应的 Handler 为 FileHandler 对象，
    然后 Handler 对象还单独指定了 Formatter 对象单独配置输出格式，
    最后给 Logger 对象添加对应的 Handler 
    然后 即可输出日志
    Formatter->Handler->Logger->Logger.debug()
    '''
    # logger的初始化工作
    logger = logging.getLogger('bytime')
    logger.setLevel(logging.DEBUG)
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'.log'
    
     # 内容格式
    contentFormat = '\r\n [ %(asctime)s ] -%(pathname)s- [ line:%(lineno)d ] -- %(levelname)s -- '
    contentFormat += '\r\n=|=\r\n %(message)s \r\n=|='
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%d-%m %p"

    # 将日志记录转化成指定的文本格式
    formmater = logging.Formatter(contentFormat, datefmt=dateFormat)

    # 添加TimedRotatingFileHandler
    # 定义一个24小时换一次log文件的handler
    # 保留3个旧log文件
    file_time_handler = logging.handlers.TimedRotatingFileHandler(fileName, when='M', interval=24, backupCount=1,encoding='utf-8')
    # 给处理器添加格式
    file_time_handler.setFormatter(formmater)
    # 设置后缀名称，跟strftime的格式一样
    # file_time_handler.suffix = "%Y-%m-%d_%H-%M-%S.log" #对应 when='S' 格式固定
    file_time_handler.suffix = "%Y-%m-%d_%H-%M.log" #对应 when='M' 格式固定
    
    # 判断handler是否已挂载到Logger对象上，已挂载则直接输出日志，未挂载则先挂载再输出日志
    if not logger.hasHandlers():
        logger.addHandler(file_time_handler)
    
    # 返回记录器对象
    return logger


if __name__ == '__main__':
    pass
    # set_log_zh('zh').debug('pendant')
