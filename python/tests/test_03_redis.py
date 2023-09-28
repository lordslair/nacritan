import os
import redis
import time

r = redis.StrictRedis(
    host=os.environ['REDIS_HOST'],
    port=6379,
    db=0,
    encoding='utf-8')


def test_nacritan_redis_connection():
    assert r.ping()


def test_nacritan_redis_set():
    assert r.set('test_nacritan', 'OK', ex=1)


def test_nacritan_redis_get():
    assert r.get('test_nacritan')


def test_nacritan_redis_expired():
    time.sleep(1)
    assert not r.get('test_nacritan')
