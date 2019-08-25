from rediscluster import StrictRedisCluster

# 配置主数据库的ip和端口号
nodes = [
    {"host": "127.0.0.1", 'port': 7000},
    {"host": "127.0.0.1", 'port': 7001},
    {"host": "127.0.0.1", 'port': 7002}
]

# 创建集群客户端
cluster = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)

# 使用集群客户端进行数据操作
cluster.set("name", 'zs')
name = cluster.get("name")
print(name)

# 集群不支持事务/乐观锁/管道/多值操作 mset mget

# 集群中如果需要处理一致性问题, 可以手动实现setnx悲观锁(分布式锁)
# setnx lock:order


# 65335槽   通过取模的方式自动分配数据库节点