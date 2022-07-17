from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from src.server.instance import server
import requests
import lyricsgenius
import uuid
from dotenv import load_dotenv
import os
from src.server.controllers.RedisCache import RedisCache
import redis
import json
from boto3 import resource

load_dotenv()

app, api = server.app, server.api
redis_cache = RedisCache()


@api.route('/app/artist/<artist_name>')
class GeniusConsume(Resource):

    def get(self,artist_name):
        cache_param = request.args.get('cache')

        cache = False if cache_param is not None and cache_param == 'False' else True

        try:
            status, artist_cache = self.get_artist(artist_name,cache)

            if not status:
                raise Exception('Nao foi possivel encontrar o artista!')

            return jsonify(
                {
                    'status': 'success',
                    'artist_name': artist_name,
                    'songs_list': artist_cache
                }
            )
        except Exception as e:
            return jsonify(
                {
                    'status': 'error',
                    'search_term': artist_name,
                    'message': str(e),
                    'artist_name': None,
                    'songs_list': []
                }
            )

    def get_artist(self,artist_name,cache):
        token = os.getenv('GENIUS_TOKEN')
        genius = lyricsgenius.Genius(token)
        list = []

        if cache:
            status, artist_cache = self.get_cache(artist_name)
            return status, artist_cache

        artist = genius.search_artist(artist_name,10, sort='popularity')

        if artist is None:
            return False, list

        id_transaction = str(uuid.uuid4())
        for i in range(len(artist.songs)):
            a = artist.songs[i]
            list.append(a.title)
        redis_cache.set_item(artist_name, list)

        try:
            dynamodb = resource(
                'dynamodb',
                region_name='us-east-2',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            table = dynamodb.Table('tb_searches')
            table.put_item(
                Item={
                    'id_transaction': id_transaction,
                    'artist': artist_name,
                    'songs': list
                }
            )
        except Exception a
        return True, list

    def get_cache (self,artist_input_name):
        artist_cache = redis_cache.get_item(artist_input_name)
        if artist_cache is not None:
            artist_cache = artist_cache.decode('utf-8')
            artist_cache = str(artist_cache).replace("'", '"')
            artist_cache = json.loads(artist_cache)
            return True, artist_cache
        return False, artist_cache










