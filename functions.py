import logging
import time
try:
    import retrying
except Exception as e:
    print('The retrying package is not installed.')
    exit()

def setLog(infoMsg='', logName='', openMethod='a+'):
    # 日志文件路径
    fileName = './'+ str(time.strftime('%Y%m%d',time.localtime()))+'-'+str(logName)+'.log'
    # 日期格式
    dateFormat = "%H:%M:%S %Y-%d-%m %p"
    # 内容格式
    contentFormat = '\r\n %(asctime)s %(pathname)s[line:%(lineno)d] -- FuncName : %(funcName)s -- %(levelname)s -- '
    contentFormat += '\r\n %(message)s'
    # 一次性基础配置
    logging.basicConfig(level=logging.DEBUG,  
                    format= contentFormat,
                    datefmt = dateFormat,
                    filename= fileName,  
                    filemode=openMethod)
    logging.debug(str(infoMsg))

