import os
from redis import Redis
from flask import Flask, request, jsonify

class RedisCache:
    def __init__(self):
        try:
            self.client = Redis(
                host=os.getenv('REDIS_HOST'),
                port=int(os.getenv('REDIS_PORT'))
            )

            self.days_expire = 60 * 60 * 24 * int(os.getenv('REDIS_DAYS_EXPIRE'))
        except Exception as e:
            print(e)

    def get_item(self, item_name):
        try:
            if self.client.exists(item_name):
                return self.client.get(item_name)
        except Exception as e:
            print(e)
        return None

    def set_item(self, item_name, item_data):

        try:
            if self.client.exists(item_name):
                self.client.delete(item_name)
            self.client.set(item_name, str(item_data))
            self.client.expire(item_name, self.days_expire)
        except Exception as e:
            print(e)