import configparser
import os

path = os.path.realpath(os.path.dirname(__file__))
config = configparser.ConfigParser(interpolation=None)
config.read(os.path.join(path, 'serv_config.ini'))

API_KEY = config.get('GOOGLE_API', 'api_key')
CUSTOM_SEARCH_ENGINE_ID = config.get('GOOGLE_API', 'custom_search_engine_id')

