import os
from django.core import serializers
from djog.settings import PROJECT_ROOT

def main():
    json_file = os.path.join(PROJECT_ROOT,'djog/serialization/file.json')
    with open(json_file, 'r') as data:
        json_data_str = data.read()
        for obj in serializers.deserialize("json", json_data_str):
            obj.save()

if __name__ == '__main__':
    main()
