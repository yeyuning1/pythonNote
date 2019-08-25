from redis.sentinel import Sentinel

# 配置哨兵的ip和端口号
sentinels = [
    ("127.0.0.1", 26380),
    ("127.0.0.1", 26381),
    ("127.0.0.1", 26382)
]

# 创建哨兵对象
sentinel = Sentinel(sentinels=sentinels)

# 主数据库的别名
service_name = 'mymaster'

# 通过哨兵来获取redis主从  优点会返回新的连接地址
redis_master = sentinel.master_for(service_name=service_name)
redis_slave = sentinel.slave_for(service_name=service_name)

# 执行数据操作
# redis_master.set('name', 'wangwu')
# name = redis_master.get('name')
# print(name)

"""
主从选择:
只是读操作, 可以直接选择从数据库
如果有读有写, 建议直接使用主数据库   可以使用乐观锁/管道
"""

name = redis_slave.get('name')
print(name)
redis_slave.set('name', 'wangwu')