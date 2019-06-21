# ProxyPool
## 最近一次更新时间 2018年11月28日
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
	- 项目启动文件/入口文件/执行文件/....(差不多就是这个意思,如果直接从redis里面读取proxy，则不需要执行run.py的api()方法)
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

1. 复制一份config.env 名称改为 config.py，作为项目配置文件，查看说明注释 config.py 修改相关配置
2. 安装项目需要的包
3. 安装 redis
4. 运行 run.py
5. 查看redis存储 代理存储默认是 0库
6. 通过ip获取代理 http://127.0.0.1:5000/get
7. 查看当前代理池中代理数量： http://127.0.0.1:5000/count


#### 项目参考
https://github.com/Germey/ProxyPool
