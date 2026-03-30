echo "invoking SAVE"
/usr/bin/redis-cli SAVE

echo "sleeping 5 secs"
sleep 5

echo "invoking SAVE"
/usr/bin/redis-cli SAVE
