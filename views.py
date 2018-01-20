from flask import jsonify,request
from flask_restful import Api,Resource,reqparse

from main import app
from api.netease import NetEase
from api.xiami import Xiami



api=Api(app)
netease=NetEase()
xiami=Xiami()

class Search(Resource):
    """
    """
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('source',type=str,required=True,
                                help='source必须',location='values')
        self.reqparse.add_argument('keywords',type=str,required=True,
                                help='keywords必须',location='values')
        self.reqparse.add_argument('ktype',type=int,default=1,location='values')
        self.reqparse.add_argument('offset',type=int,default=0,location='values')
        self.reqparse.add_argument('limit',type=int,default=60,location='values')
        super().__init__()


    def get(self):
        args=self.reqparse.parse_args(strict=True)
        source=args['source']
        keywords=args['keywords']
        ktype=args['ktype']
        offset=args['offset']
        limit=args['limit']
        if source=='netease':
            # 网易云
            result=netease.search(keywords,ktype,offset,limit)
        elif source=='xiami':
            result=xiami.search(keywords)
        else:
            result={}
        return jsonify(result)


class Playlists(Resource):
    """
    获取歌单
    """
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('source',type=str,required=True,
                                help='source必须',location='values')
        self.reqparse.add_argument('page',type=int,default=1,location='values')
        self.reqparse.add_argument('cat',type=str,default='全部',location='values')
        self.reqparse.add_argument('order',type=str,default='hot',location='values')
        self.reqparse.add_argument('offset',type=int,default=0,location='values')
        self.reqparse.add_argument('limit',type=int,default=50,location='values')
        super().__init__()


    def get(self):
        args=self.reqparse.parse_args(strict=True)
        source=args['source']
        page=args['page']
        category=args['cat']
        order=args['order']
        offset=args['offset']
        limit=args['limit']
        if source=='netease':
            result=netease.playlists(category,order,offset,limit)
        elif source=='xiami':
            result=xiami.playlists(page,limit)
        else:
            result={}
        return jsonify(result)


class PlaylistDetail(Resource):
    """
    根据歌单id获取歌单详情
    """
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('source',type=str,required=True,
                                help='source必须',location='values')
        self.reqparse.add_argument('id',type=str,required=True,
                                help='歌单id必须',location='values')
        super().__init__()


    def get(self):
        args=self.reqparse.parse_args(strict=True)
        source=args['source']
        id=args['id']
        if source=='netease':
            result=netease.playlist_detail(id)
        elif source=='xiami':
            result=xiami.playlists_detail(id)
        else:
            result={}
        return jsonify(result)


class SongUrl(Resource):
    """
    根据歌曲id获取歌曲url
    """
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('source',type=str,required=True,
                                help='source必须',location='values')
        self.reqparse.add_argument('id',type=str,required=True,
                                help='歌曲id必须',location='values')
        super().__init__()


    def get(self):
        args=self.reqparse.parse_args(strict=True)
        source=args['source']
        id=args['id']
        if source=='netease':
            result=netease.song_url(id)
        elif source=='xiami':
            result=xiami.song_url(id)
        else:
            result={}
        return jsonify(result)


class Lyric(Resource):
    """
    根据歌曲id获取歌词
    """
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('source',type=str,required=True,
                                help='source必须',location='values')
        self.reqparse.add_argument('id',type=str,required=True,
                                help='歌曲id必须',location='values')
        super().__init__()
    
    def get(self):
        args=self.reqparse.parse_args(strict=True)
        source=args['source']
        id=args['id']
        if source=='netease':
            result=netease.lyric(id)
        elif source=='xiami':
            result=xiami.lyric(id)
        else:
            result={}
        return jsonify(result)


class FM(Resource):
    """
    网易云音乐私人FM
    """
    def __init__(self):
        super().__init__()

    def get(self):
        result=netease.person_fm()
        return jsonify(result)


api.add_resource(Search,'/search')
api.add_resource(Playlists,'/playlists')
api.add_resource(PlaylistDetail,'/playlist/detail')
api.add_resource(SongUrl,'/music/url')
api.add_resource(Lyric,'/lyric')
api.add_resource(FM,"/fm")
    