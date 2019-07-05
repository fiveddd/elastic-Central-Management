# elastic-Central-Management

## 说明

该项目的主要目的是提供一个可视化的操作界面来对elastic集群进行维护，包括配置修改，集群升级等功能。

主要目的为：
- 让运维人员能够方便快捷的对elastic集群进行维护
- 面向用户界面，而非面向大量的ansible脚本
- 只要能访问web UI即可对集群进行运维，不需要在本地安装ansible和下载大量的ansible脚本


该项目采用前后端分离的方式，前端使用了iview admin，后端使用了python + ansible

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190705105607572.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9sZXgtbGVlLmJsb2cuY3Nkbi5uZXQ=,size_16,color_FFFFFF,t_70)

## 用法

下载：
```shell
git clone https://github.com/oldcodeoberyn/elastic-Central-Management.git
```

注意：目前还属于POC阶段，代码会持续变动。

### dev

```shell
cd elastic-Central-Management
python3 webservice.py
cd frontend
npm run dev
```

然后访问 http://localhost:8081/

### dev

```shell
cd elastic-Central-Management
python3 webservice.py
cd frontend
npm run build
```

然后访问 http://localhost:3389/



