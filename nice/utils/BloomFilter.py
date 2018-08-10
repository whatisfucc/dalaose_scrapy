# -*- coding: utf-8 -*-

import redis
from hashlib import md5
from nice.config import FILTER_DB, FILTER_HOST, FILTER_PASS


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class BloomFilter(object):
    def __init__(self, host=FILTER_HOST, port=6379, db=FILTER_DB, password=FILTER_PASS, blockNum=1, key='filter_list'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.server = redis.Redis(host=host, port=port, db=db, password=password)
        self.bit_size = 1 << 25
        self.seeds = [5, 7, 11, 13, 31]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def is_contains(self, str_input):
        if not str_input:
            return False
        if isinstance(str_input, str):
            str_input = str_input.encode('utf8')
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        if isinstance(str_input, str):
            str_input = str_input.encode('utf8')
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


if __name__ == '__main__':
    bf = BloomFilter()
    if bf.is_contains('2d1d7ebf07048377b09f4aee58df6ecf'):  # 判断字符串是否存在
        print('exists!')
    else:
        print('not exists!')
        # bf.insert('http://www.baidu.com')
    # for x in xrange(10000, 111111):
    #     bf.insert(str(x))
