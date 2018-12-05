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
    proxy: '' 代理ip
    retry: False 是否是重试请求
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
        # print('Get Proxies From Url -> ', url, r.status_code)
        if r.status_code == requests.codes.ok:
            r.encoding='utf-8'
            return r.text
    except Exception as e:
        pass
        # 无代理 并且重试还失败则记录日志 - 有代理的情况下多数是代理连接失败
        if retry and not proxy:
            set_log_zh_bytime('request_proxy').debug('{}\r\n{}'.format(url,e))
  


def set_log(logname, openmethod='a+'):
    ''' 
    简单记录英文日志
    logname: 日志文件标识
    openmethod: a+ 日志读写方式
    '''
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'_dug.log'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%m-%d %p"
    # 内容格式
    contentFormat = '\r\n [ %(asctime)s ] -%(pathname)s- [ line:%(lineno)d ] -- %(levelname)s -- '
    contentFormat += '\r\n %(message)s'
    # 一次性基础配置
    logging.basicConfig(level=logging.DEBUG,  
                    format= contentFormat,
                    datefmt = dateFormat,
                    filename= fileName,  
                    filemode=openmethod)
    return logging


def set_log_bybytes(logname, maxbytes=1048576, backupCount=1, openmethod='a+'):
    '''
    记录中文日志-按大小切割
    logname: 日志文件标识
    maxbytes: 1048576 日志大小 bytes
    backupCount 1 备份文件个数 
    openmethod:  a+ 日志读写方式 
    '''

    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'_zh.log'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%m-%d %p"
    # 内容格式
    contentFormat = '\r\n [ %(asctime)s ] -%(pathname)s- [ line:%(lineno)d ] -- %(levelname)s -- '
    contentFormat += '\r\n %(message)s'

    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    
    formmater = logging.Formatter(contentFormat, datefmt=dateFormat)
    
    handler = logging.handlers.RotatingFileHandler(fileName, mode=openmethod, maxBytes=1048576, backupCount=1, encoding='utf-8', delay=False)
    handler.setFormatter(formmater)
   
    if file_time_handler not in logger.handlers:
        logger.addHandler(file_time_handler)
    
    return logger
    
    


def set_log_zh_bytime(logname):
    '''
    按时间分割记录中文日志
    logname: 日志文件标识
    '''
    logger = logging.getLogger(logname)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'_byTime.log'
    # 内容格式
    contentFormat = '\r\n [ %(asctime)s ] -%(pathname)s- [ line:%(lineno)d ] -- %(levelname)s -- '
    contentFormat += '\r\n %(message)s'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%m-%d %p"

    formmater = logging.Formatter(contentFormat, datefmt=dateFormat)

    file_time_handler = logging.handlers.TimedRotatingFileHandler(fileName, when='S', interval=5, backupCount=3,encoding='utf-8')
    file_time_handler.setFormatter(formmater)
    # file_time_handler.suffix = "%Y-%m-%d_%H-%M-%S.log" #对应 when='S' 格式固定
    file_time_handler.suffix = "%Y-%m-%d_%H-%M-%S.log" #对应 when='H' 格式固定
    
    logger.addHandler(file_time_handler)

    return logger


if __name__ == '__main__':
    pass
    

