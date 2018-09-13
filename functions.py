import time
import logging
import logging.handlers
try:
    import retrying
except Exception as e:
    print('The retrying package is not installed.')
    exit()

def set_log(info='', logname='', funcname='set_log', openmethod='a+'):
    ''' 
    记录日志
    info: 信息
    funcname: 方法名
    logname: 日志文件标识
    openmethod: 日志读写方式
    '''
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'.log'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%d-%m %p"
    # 内容格式
    contentFormat = '\r\n %(asctime)s %(pathname)s[line:%(lineno)d] -- FuncName : '+str(funcname)+' -- %(levelname)s -- '
    contentFormat += '\r\n %(message)s'
    # 一次性基础配置
    logging.basicConfig(level=logging.DEBUG,  
                    format= contentFormat,
                    datefmt = dateFormat,
                    filename= fileName,  
                    filemode=openmethod)
    logging.debug(str(info))


def set_log_zh(info='', logname='', funcname='set_log_zh', openmethod='a+'):
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'.log'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%d-%m %p"
    # 内容格式
    contentFormat = '\r\n %(asctime)s %(pathname)s[line:%(lineno)d] -- FuncName : '+str(funcname)+' -- %(levelname)s -- '
    contentFormat += '\r\n %(message)s'

    # 1、logger对象：负责产生日志，然后交给Filter过滤，然后交给不同的Handler输出
    logger = logging.getLogger('zh') #获得一个logger对象，默认是root
    logger.setLevel(logging.DEBUG)
    #2、Filter对象：不常用，略

    #3、Handler对象：接收logger传来的日志，然后控制输出
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'-zh.log'
    handler = logging.FileHandler(fileName,openmethod,encoding='utf-8') 
    #4、Formatter对象：日志格式
    formmater = logging.Formatter(contentFormat,#'%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                        datefmt=dateFormat)

    #5、为Handler对象绑定格式
    handler.setFormatter(formmater)

    #6、将Handler添加给logger并设置日志级别
    #
    while logger.hasHandlers():
        for i in logger.handlers:
            print(i)
            logger.removeHandler(i)

    logger.addHandler(handler)
    

    #7、测试
    logger.debug(str(info))


def tt(info='', logname='', funcname='set_log_zh'):

    # 初始化日志器logger，生成处理器handler，格式化日志内容为文本，给处理器(handler)设置格式化后的文本内容，将处理器挂载到日志器looger上
    # logger的初始化工作
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+str(logname)+'.log'
    
     # 内容格式
    contentFormat = '\r\n %(asctime)s %(pathname)s[line:%(lineno)d] -- -- %(levelname)s -- '
    contentFormat += '\r\n %(message)s'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%d-%m %p"

    # 将日志记录转化成指定的文本格式
    formmater = logging.Formatter(contentFormat, datefmt=dateFormat)

    # 添加TimedRotatingFileHandler
    # 定义一个1秒换一次log文件的handler
    # 保留3个旧log文件
    filehandler = logging.handlers.TimedRotatingFileHandler(fileName, when='S', interval=1, backupCount=1,encoding='utf-8')
    # 给处理器添加格式
    filehandler.setFormatter(formmater)
    # 设置后缀名称，跟strftime的格式一样
    filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log" #对应 when='S'
    # filehandler.suffix = "%Y-%m-%d_%H-%M.log" #对应 when='M'
    
    # 把handler挂载 到looger上
    logger.addHandler(filehandler)
    # 输出日志
    logger.debug("啦啦啦")


if __name__ == '__main__':
  
    help(logging.Formatter)
    exit()
    tt()
