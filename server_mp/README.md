## 操作

#### 安装
```angular2html
pip install Scrapy
pip3 install --upgrade scrapy --trusted-host pypi.douban.com
scrapy startproject server_mp
scrapy genspider example example.com

pip install scrapyd
pip3 install scrapyd-client
```

#### 运行
```angular2html
scrapyd

构建
scrapyd-deploy -p server_mp
```



#### 测试
```angular2html
scrapy crawl news

curl http://localhost:6800/schedule.json -d project=server_mp -d spider=news
```


#### url
```angular2html
http://localhost:6800/jobs
http://127.0.0.1:6800/listprojects.json
```