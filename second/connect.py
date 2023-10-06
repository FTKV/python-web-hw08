import configparser

from mongoengine import connect


config = configparser.ConfigParser()
config.read('second/config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

client_mongo = connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}""", ssl=True)
