import logging
import time
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

