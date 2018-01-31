# -*- coding: utf-8 -*-

"""
虾米音乐api
"""

import json
import logging
from urllib import request,parse,error


logger=logging.getLogger('MyCloudMusic:'+__name__)

# 歌曲url破解，基于https://github.com/Flowerowl/xiami
def caesar(location):
    num=int(location[0])
    avg_len=int(len(location[1:])/num)
    remainder=int(len(location[1:])%num)
    result=[
        location[i*(avg_len+1)+1:(i+1)*(avg_len+1)+1]
        for i in range(remainder)
    ]
    result.extend([location[(avg_len + 1) * remainder:][i * avg_len + 1: (i + 1) * avg_len + 1] for i in range(num-remainder)])
    url=parse.unquote(
        ''.join([
            ''.join([result[j][i] for j in range(num)])
            for i in range(avg_len)
        ])+
        ''.join([result[r][-1] for r in range(remainder)])
    ).replace('^','0')
    return url


class Xiami():
    """
    """
    def __init__(self):
        self.header={
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            #'Host':'www.xiami.com',
            'Referer':'http://m.xiami.com/',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    
    def http_request(self,method,url,query=None,timeout=None):
        response=json.loads(
            self.raw_http_request(method,url,query,timeout)
        )
        return response


    def raw_http_request(self,method,url,query=None,timeout=None):
        if method=='GET':
            if query is None:
                req=request.Request(url,headers=self.header)
            else:
                params=parse.urlencode(query).encode('utf-8')
                req=request.Request(url+params,headers=self.header)
        elif method=='POST':
            data=parse.urlencode(query).encode('utf-8')
            req=request.Request(url,headers=self.header,data=data)

        response=request.urlopen(req,timeout=timeout)
        #print(response.read().decode('utf-8'))
        return response.read().decode('utf-8')


    def search(self,keywords):
        """
        搜索
        """
        keywords=parse.quote(keywords.encode('utf-8'))
        url = 'http://api.xiami.com/web?v=2.0&app_key=1&key=' + keywords \
        + '&page=1&limit=50&_ksTS=1459930568781_153&callback=jsonp154' + \
        '&r=search/songs'
        response=self.raw_http_request('GET',url)
        response = json.loads(response[len('jsonp154('):-len(')')])
        # print(data)
        return response


    def playlists(self,page=1,limit=60):
        """
        歌单          
        """
        url='http://api.xiami.com/web?v=2.0&app_key=1&_ksTS=1459927525542_91' + \
            '&page={}&limit={}&callback=jsonp92&r=collect/recommend'.format(page,limit)
        response=self.raw_http_request('GET',url)
        response= json.loads(response[len('jsonp92('):-len(')')])
        return response['data']


    def playlists_detail(self,playlist_id):
        """
        歌单详情,返回音乐标题，歌手，专辑，音乐id，音乐图片url
        """
        url = 'http://api.xiami.com/web?v=2.0&app_key=1&id={}'.format(playlist_id) + \
            '&_ksTS=1459928471147_121&callback=jsonp122&r=collect/detail'
        response=self.raw_http_request('GET',url)
        response = json.loads(response[len('jsonp122('):-len(')')])
        # 解析
        songs=[]
        for item in response['data']['songs']:
            song={
                'song_name':item['song_name'],
                'singers':item['singers'],
                'album_name':item['album_name'],
                'song_id':item['song_id'],
                'pic_url':item['album_logo']
            }
            songs.append(song)
        return songs


    def song_url(self,song_id):
        """
        根据歌曲id获取歌曲url
        """
        url = 'http://www.xiami.com/song/playlist/id/{}'.format(song_id) + \
            '/object_name/default/object_id/0/cat/json'
        response=self.raw_http_request('GET',url)
        result = json.loads(response)['data']['trackList'][0]['location']
        return caesar(result)


    def lyric(self,song_id):
        """

        """
        pass


