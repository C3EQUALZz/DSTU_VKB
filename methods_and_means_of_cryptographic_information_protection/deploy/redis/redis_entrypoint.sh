#!/bin/sh
set -e

mkdir -p /usr/local/etc/redis &&
echo "bind 0.0.0.0" > /usr/local/etc/redis/redis.conf &&
echo "requirepass $REDIS_PASSWORD" >> /usr/local/etc/redis/redis.conf &&
echo "appendonly yes" >> /usr/local/etc/redis/redis.conf &&
echo "appendfsync everysec" >> /usr/local/etc/redis/redis.conf &&
echo "user default on nopass ~* +@all" > /usr/local/etc/redis/users.acl &&
echo "user $REDIS_USER on >$REDIS_USER_PASSWORD ~* +@all" >> /usr/local/etc/redis/users.acl &&
redis-server /usr/local/etc/redis/redis.conf --aclfile /usr/local/etc/redis/users.acl