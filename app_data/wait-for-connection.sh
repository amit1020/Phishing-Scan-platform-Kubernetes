#!/bin/sh
# wait-for-it.sh, try to connects the database 

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port to be available..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "$host:$port is available! Starting application..."
exec $cmd  
