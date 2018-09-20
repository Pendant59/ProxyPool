from main import Main
from multiprocessing import Process
from api import app
 
def run():
    get_process = Process(target=Main.GrabProxies)
    check_process = Process(target=Main.CheckProxies)
    get_process.start()
    check_process.start()

def api():
	app.run()

if __name__ == '__main__':
	# 抓取和检测
	run()
	# 提供proxy的接口
	api()