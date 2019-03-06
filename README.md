## 微信文章爬虫

### 服务器
- 服务器：A03
- 位置：/data/www/yunfu/sddl/crawler
- 爬取的图片放到a03 /data/www/yunfu/sddl/tech/storage/news
- tmux：sddl_crawler_wechat
- 运行命令：python36 main.py
#### tmux(sddl_crawler_wechat)
- tmux new -s sddl_crawler_wechat
- tmux a -t sddl_crawler_wechat
- tmux detach
- tmux ls
- tmux kill-session -t sddl_crawler_wechat

----------

### 数据库名称
- wechat_article

----------

### python依赖文件安装
- requirements.txt安装

----------

### 配置文件说明
- 配置文件位置：config_default.py
- next_turn_seconds:运行整个轮次结束后休息多少秒后进行下一次
- db：数据库配置
- weixinhao：微信公众号列表


### 接入了云打码服务, verification_code文件夹
