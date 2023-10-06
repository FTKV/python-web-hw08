import configparser

from mongoengine import connect
import redis
from redis_lru import RedisLRU


config = configparser.ConfigParser()
config.read('first/config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

client_mongo = connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}""", ssl=True)

try:

    client_redis = redis.Redis(host='localhost',
                 port=6379,
                 db=0)
    client_redis.ping()  # This will attempt to ping the server, and if successful, you're connected.
    cache = RedisLRU(client_redis)
except redis.ConnectionError:
    print("Could not connect to Redis")