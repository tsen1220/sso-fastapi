import redis
import json
from typing import Optional
from fastapi import Depends
from app import get_redis

class RedisHelper:
    def __init__(self, redis: redis.Redis = Depends(get_redis)):
        self.redis = redis

    def set(self, key: str, value: any, ex: Optional[int] = None) -> bool:
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            self.redis.set(key, value, ex=ex)

            return True
        except Exception as e:
            print(f"Redis Set Error: {e}")
            return False

    def get(self, key: str) -> Optional[str]:
        try:
            value = self.redis.get(key)
            if value is None:
                return None
            
            return value
        except Exception as e:
            print(f"Redis Get Error: {e}")
            return None

    def delete(self, key: str) -> bool:
        try:
            return self.redis.delete(key) > 0
        except Exception as e:
            print(f"Redis Delete Error: {e}")
            return False

    def exists(self, key: str) -> bool:
        try:
            return self.redis.exists(key) > 0
        except Exception as e:
            print(f"Redis Exists Error: {e}")
            return False

    def expire(self, key: str, seconds: int) -> bool:
        try:
            return self.redis.expire(key, seconds)
        except Exception as e:
            print(f"Redis Expire Error: {e}")
            return False

    ### list ###

    def lpush(self, key: str, *values) -> int:
        try:
            return self.redis.lpush(key, *values)
        except Exception as e:
            print(f"Redis LPush Error: {e}")
            return -1

    def rpush(self, key: str, *values) -> int:
        try:
            return self.redis.rpush(key, *values)
        except Exception as e:
            print(f"Redis RPush Error: {e}")
            return -1

    def lpop(self, key: str) -> Optional[str]:
        try:
            return self.redis.lpop(key)
        except Exception as e:
            print(f"Redis LPop Error: {e}")
            return None

    def rpop(self, key: str) -> Optional[str]:
        try:
            return self.redis.rpop(key)
        except Exception as e:
            print(f"Redis RPop Error: {e}")
            return None

    def lrange(self, key: str, start: int, end: int) -> list[str]:
        try:
            return self.redis.lrange(key, start, end)
        except Exception as e:
            print(f"Redis LRange Error: {e}")
            return []
        
    ### hash map ###

    def hset(self, name: str, key: str, value: str) -> bool:
        try:
            return self.redis.hset(name, key, value) > 0
        except Exception as e:
            print(f"Redis HSet Error: {e}")
            return False

    def hget(self, name: str, key: str) -> Optional[str]:
        try:
            return self.redis.hget(name, key)
        except Exception as e:
            print(f"Redis HGet Error: {e}")
            return None

    def hdel(self, name: str, key: str) -> bool:
        try:
            return self.redis.hdel(name, key) > 0
        except Exception as e:
            print(f"Redis HDel Error: {e}")
            return False

    def hgetall(self, name: str) -> dict[str, str]:
        try:
            return self.redis.hgetall(name)
        except Exception as e:
            print(f"Redis HGetAll Error: {e}")
            return {}
        
    ### Sorted Set (ZSet) ###
    
    def zadd(self, name: str, mapping: dict[str, float]) -> bool:
        try:
            return self.redis.zadd(name, mapping) > 0
        except Exception as e:
            print(f"Redis ZAdd Error: {e}")
            return False

    def zrange(self, name: str, start: int, end: int, withscores: bool = False) -> list[tuple[str, float]]:
        try:
            return self.redis.zrange(name, start, end, withscores=withscores)
        except Exception as e:
            print(f"Redis ZRange Error: {e}")
            return []

    def zremove(self, name: str, member: str) -> bool:
        try:
            return self.redis.zrem(name, member) > 0
        except Exception as e:
            print(f"Redis ZRem Error: {e}")
            return False