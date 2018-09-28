# ProxyPool

#### 项目介绍
- 基于Python3.6的自建代理池
- An proxy pool module implemented by Python3.6
- Github 开源地址：https://github.com/Pendant59/ProxyPool
- Gitee 码云开源地址：https://gitee.com/pendant/ProxyPool

#### 可能需要自己安装的包/项目需要的包
- pyquery
- asyncio
- aiohttp
- redis

#### 模块说明

- run.py
	- 项目执行文件/入口文件/....差不多就是这个意思
- main.py
	- 主控制器/调度器模块
		- class Main 主程序类，控制代理的抓取和检测
		- class DoGrab 抓取代类，负责抓取代理
		- class DoCheck 代理检测类，负责检测代理
- api.py
	- api模块，启动一个Web服务器，使用Flask实现，对外提供代理的获取功能
- getdata.py
	- 爬虫模块
		- class GetProxiesData 爬取代理类，提供各网站代理的抓取功能
- db.py
	- redis操作模块
		- class RedisClient 连接以及操作redis，提供代理入库、提取功能
- bloomfilter.py
	- 代理去重复模块
		- class BloomFilter 查重类
		- class SimpleHash 简单hash函数类
- functions.py
	- 函数模块
- config.py
	- 项目配置模块

#### 使用说明

1. 查看项目配置文件 config.py 修改相关配置
2. 安装项目需要的包
3. 安装 redis
4. 运行 run.py
5. 查看日志文件以及redis存储 代理存储默认是 0库


#### 项目参考
https://github.com/Germey/ProxyPool
