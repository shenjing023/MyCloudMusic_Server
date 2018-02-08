# MyCloudMusic_Server
MyCloudMusic的服务端，基于flask

# 安装
1. clone代码到本地
```
git clone https://github.com/shenjing023/MyCloudMusic_Server.git
```
2. 安装virtualenv
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```
3. 安装依赖
```
cd MyCloudMusic_Server
pip install -r requirements.txt
```
4. 启动服务
```
python manage.py server
```
地址：http://127.0.0.1:5000
# 接口文档
## 搜索
**说明:** 网易云：搜索单曲、歌手、专辑、歌单、用户 ; 虾米：搜索单曲

**必选参数:** *source* :数据源(netease网易云，xiami虾米); *keywords*:关键词

**可选参数:** 网易云：ktype(搜索类型，单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002))，offset(偏移数量，用于分页),limit(返回数量 , 默认为60)

**接口地址:** /search

**调用例子:** /search?source=netease&keywords=123
## 获取精选歌单
**说明:** 歌单（网友精选碟）

**必选参数:** *source* :数据源(netease网易云，xiami虾米)

**可选参数:** 网易云:cat(歌单类型，" 华语 "、" 古风 " 、" 欧美 "、" 流行 ", 默认为 " 全部 ")，order(歌单排列类型，默认"hot")，offset(偏移数量，用于分页),limit(返回数量 , 默认为50); 虾米:page(歌单页码，用于分页,默认为1),limit(返回数量 , 默认为50);

**接口地址:** /playlists

**调用例子:** /playlists?source=netease
## 获取歌单详情
**说明:** 根据歌单id获取歌单详情

**必选参数:** *source* :数据源(netease网易云，xiami虾米)，*id*: 歌单id号

**接口地址:** /playlist/detail

**调用例子:** /playlist/detail?source=netease&id=xxxxxxx
## 获取音乐url
**说明:** 根据歌曲id获取歌曲url

**必选参数:** *source* :数据源(netease网易云，xiami虾米)，*id*: 歌曲id号

**接口地址:** /music/url

**调用例子:** /music/url?source=netease&id=xxxxxxx
## 获取歌词
**说明:** 根据歌曲id获取歌词

**必选参数:** *source* :数据源(netease网易云，xiami虾米)，*id*: 歌曲id号

**接口地址:** /lyric

**调用例子:** /lyric?source=netease&id=xxxxxxx
## 私人FM
**说明:** 网易云私人FM

**接口地址:** /fm

**调用例子:** /fm
# 简易客户端
[MyCloudMusic](https://github.com/shenjing023/MyCloudMusic)
# 致谢
在开发过程中，参考了很多音乐网站API的分析代码和文章，感谢这些开发者的努力。（具体项目网址参考源码）
# License
GNU GENERAL PUBLIC LICENSE Version 2



