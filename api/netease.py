# -*- coding: utf-8 -*-

"""
网易云音乐api
"""

import os
import base64
import random
import hashlib
import json
import logging
import binascii
from urllib import request,parse,error

from Crypto.Cipher import AES

logger=logging.getLogger('MyCloudMusic:'+__name__)

DEFAULT_TIMEOUT=10

MODULUS = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b72' + \
    '5152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbd' + \
    'a92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe48' + \
    '75d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
NONCE = '0CoJUm6Qyw8W8jud'
PUBKEY = '010001'

# 歌曲加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic脚本实现
def _encrypted_id(id):
    magic=bytearray('3go8&$8*3*3h0k(2)2','u8')
    song_id=bytearray(id,'u8')
    magic_len=len(magic)
    for i,sid in enumerate(song_id):
        song_id[i]=sid^magic[i%magic_len]
    m=hashlib.md5(song_id)
    result=m.digest()
    result=base64.b64encode(result)
    result=result.replace(b'/',b'_')
    result=result.replace(b'+',b'-')
    return result.decode('utf-8')


def _aes_encrypt(text,sec_key):
    pad=16-len(text)%16
    text=text+chr(pad)*pad
    encryptor=AES.new(sec_key,2,'0102030405060708')
    cipher_text=encryptor.encrypt(text)
    cipher_text=base64.b64encode(cipher_text).decode('utf-8')
    return cipher_text


def _rsa_encrypt(text,pub_key,modulus):
    text=text[::-1]
    rs=pow(int(binascii.hexlify(text),16),int(pub_key,16),int(modulus,16))
    return format(rs,'x').zfill(256)


def _create_secret_key(size):
    return binascii.hexlify(os.urandom(size))[:16]


def _encrypted_request(text):
    text=json.dumps(text)
    sec_key=_create_secret_key(16)
    enc_text=_aes_encrypt(_aes_encrypt(text,NONCE),sec_key)
    enc_sec_key=_rsa_encrypt(sec_key,PUBKEY,MODULUS)
    data={
        'params':enc_text,
        'encSecKey':enc_sec_key
    }
    return data


class NetEase():
    """
    """
    def __init__(self):
        self.header={
            'Accept':'*/*',
            #'Accept-Encoding':'gzip,deflate,sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'music.163.com',
            'Referer':'http://music.163.com/search',
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
        
        return response.read().decode('utf-8')


    def recommend_playlist(self):
        """
        每日推荐歌单
        """
        try:
            url='http://music.163.com/weapi/v1/discovery/recommend/songs?csrf_token='
        except error.HTTPError as e:
            logger.error(e)


    def person_fm(self):
        """
        私人FM
        """
        url='http://music.163.com/api/radio/get'
        try:
            data=self.http_request('GET',url)
            return data['data']
        except error.HTTPError as e:
            logger.error(e)
            return False

    
    def search(self,keywords,ktype=1,offset=0,limit=60):
        """
        搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
        """
        url='http://music.163.com/api/search/get'
        data={
            's':keywords,
            'type':ktype,
            'offset':offset,
            'total':'true' if offset else 'false',
            'limit':limit
        }
        return self.http_request('POST',url,data,timeout=DEFAULT_TIMEOUT)


    def playlists(self,category='全部',order='hot',offset=0,limit=50):
        """
        歌单（网友精选碟） hot||new http://music.163.com/#/discover/playlist/
        """
        category=parse.quote(category.encode('utf-8'))
        url='http://music.163.com/api/playlist/list?cat={}&order={}&offset={}&total={}&limit={}'.format(
            category,order,offset,'true' if offset else 'false',limit
        )
        try:
            data=self.http_request('GET',url,timeout=DEFAULT_TIMEOUT)
            # 解析
            result=[]
            for item in data['playlists']:
                d={
                    'collect_name':item['name'],
                    'list_id':item['id'],
                    'logo':item['coverImgUrl']
                }
                result.append(d)
            return result
        except error.HTTPError as e:
            logger.error(e)
            return []


    def playlist_detail(self,playlist_id):
        """
        根据歌单id获取歌单详情，返回音乐标题，歌手，专辑，音乐id，音乐图片url
        使用新版本v3接口，
        借鉴自https://github.com/Binaryify/NeteaseCloudMusicApi/commit/a1239a838c97367e86e2ec3cdce5557f1aa47bc1
        """
        url='http://music.163.com/weapi/v3/playlist/detail'
        data={
            'id':playlist_id,
            'total':'true',
            'csrf_token':'',
            'limit':1000,
            'n':1000,
            'offset':0
        }
        data=_encrypted_request(data)
        response=self.http_request('POST',url,data,timeout=DEFAULT_TIMEOUT)
        # 解析
        songs=[]
        for item in response['playlist']['tracks']:
            song_name=item['name']  # 音乐名称
            # 歌手
            for singer in item['ar']:
                singers=singer['name']
                singers+='/'
            singers=singers[:-1]
            # 专辑,图片url
            album=item['al']['name']
            pic_url=item['al']['picUrl']
            # 歌曲id
            song_id=item['id']

            song={
                'song_name':song_name,
                'singers':singers,
                'album_name':album,
                'song_id':song_id,
                'pic_url':pic_url
            }
            songs.append(song)

        return songs


    def song_url(self,song_id,bit_rate=320000):
        """
        根据歌曲id获取歌曲url
        """
        url='http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        data={
            'ids':[song_id],
            'br':bit_rate,
            'csrf_token':''
        }
        data=_encrypted_request(data)
        result=self.http_request('POST',url,data,timeout=DEFAULT_TIMEOUT)
        return result['data'][0]


    def album(self,album_id):
        """
        专辑
        """
        url='http://music.163.com/api/album/{}'.format(album_id)
        try:
            result=self.http_request('GET',url)
            return result['album']['songs']
        except error.HTTPError as e:
            logger.error(e)
            return []


    def lyric(self,song_id):
        """
        歌词
        """
        url='http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
        try:
            data=self.http_request('GET',url)
            if 'lrc' in data and data['lrc']['lyric'] is not None:
                lyric_info = data['lrc']['lyric']
            else:
                lyric_info = '未找到歌词'
            return {'info':lyric_info}
        except error.HTTPError as e:
            logger.error(e)
            return {}





