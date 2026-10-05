#!/bin/bash
set -e

# Start MySQL in background using the official entrypoint
/usr/local/bin/docker-entrypoint.sh mysqld &
MYSQL_PID=$!

echo "Waiting for replica MySQL to be ready..."
until mysqladmin ping -u root -p"${MYSQL_ROOT_PASSWORD}" --silent 2>/dev/null; do
  sleep 2
done

echo "Waiting for primary MySQL to be ready..."
until mysql -h mysql-primary -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1" >/dev/null 2>&1; do
  sleep 2
done

echo "Configuring replication..."
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<-EOSQL
  STOP REPLICA;
  CHANGE REPLICATION SOURCE TO
    SOURCE_HOST='mysql-primary',
    SOURCE_USER='replicator',
    SOURCE_PASSWORD='replicator',
    SOURCE_AUTO_POSITION=1,
    GET_SOURCE_PUBLIC_KEY=1;
  START REPLICA;
EOSQL

echo "Replication active."
wait $MYSQL_PID
