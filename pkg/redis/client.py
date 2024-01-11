import redis

class RedisClient:

    def __init__(self, host="localhost", port=6379, password=None):
        self.client = redis.Redis(host=host, port=port, password=password)

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value):
        return self.client.set(key, value)

    def exists(self, key):
        return self.client.exists(key)
    
    def setx(self, key, value, ex):
        return self.client.setex(key, ex, value)