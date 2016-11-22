import os
from django.core import serializers
from cartridge.shop.models import Product, ProductImage, ProductVariation
from djog.settings import PROJECT_ROOT


def main():
    json_file = os.path.join(PROJECT_ROOT,'djog/serialization/file.json')
    with open(json_file, "w") as out:
        json_serializer = serializers.get_serializer('json')()
        all_objects = (list(Product.objects.all()) + list(ProductImage.objects.all()) +
                       list(ProductVariation.objects.all()))
        json_serializer.serialize(all_objects, stream=out)

if __name__ == '__main__':
    main()
