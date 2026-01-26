#!/bin/sh
set -e
mv "/app/flag" "/app/flag-$(head -c 16 /dev/urandom | xxd -p)"

for i in $(seq 1 100)
do
  echo "DH{fake_flag}" > /app/flag-$(head -c 16 /dev/urandom | xxd -p)
done

exec socat TCP-LISTEN:5000,reuseaddr,fork EXEC:./main,nofork,stderr