from flask import Flask, g
from config import GET_PROXY_TYPE
from db import RedisClient

__all__ = ['app']

app = Flask(__name__)


def redis():
    """
    在没有连接redis的情况下，建立新的连接，已连接则不重新创建连接
    Opens a new redis connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = RedisClient()
    return g.db


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2><br>'


@app.route('/get')
def getProxy():
    """
    Get a proxy
    """
    db = redis()
    proxyDict = db.getOnceProxy() if GET_PROXY_TYPE is 0 else db.getProxy()
    proxyStr = '|'+proxyDict['http']+'|'
    return proxyStr



@app.route('/count')
def getProxyLength():
    """
    Get the count of proxies
    """
    db = redis()
    length = db.getProxyLength
    return str(length)


if __name__ == '__main__':
    app.run()
