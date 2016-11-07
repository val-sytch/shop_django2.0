import os
from datetime import datetime
from io import BytesIO
from random import choice
from googleapiclient.discovery import build
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from configs.config import (IMG_WIDTH_REQUIR, IMG_HEIGHT_REQUIR,
                            WATERMARK, WATERMARK_OPACITY, NUMBER_IMG_REQUIR)
from configs.services_config.serv_config import API_KEY, CUSTOM_SEARCH_ENGINE_ID
from cartridge.shop.models import Product, ProductImage, ProductVariation
from djog.settings import MEDIA_ROOT
from services.img_resizer_and_watermark_add import img_resizer_and_watermark_add
from services.parser_dog_breeds import parser_breeds, breeds_links_read
from django.utils import timezone

PRICE_CHOICES = [5, 10, 15, 20, 25, 30]


def request_to_google_cse(api_key, query, custom_search_engine_id, number_img_requir):
    """
    Make a request to google custom search API.
    Google API Client Library for Python is used.
    :param api_key: the key query parameter to identify your application.
    :param query: query parameter to specify your search expression.
    :param custom_search_engine_id: specify the custom search engine you want to use to perform
    this search. (used 'cx' for a search engine created with the Control Panel)
    :param number_img_requir: required number of links that you need
    :return: data in JSON format. To access each link use: links['items'][i]['link']
    """
    service = build("customsearch", "v1",
                developerKey=api_key)
    links = service.cse().list(
        q=query,
        cx=custom_search_engine_id,
        fileType='jpg,png',
        imgSize='xxlarge',
        num=number_img_requir,
        searchType='image',
        fields='items/link'
        ).execute()
    return links


def download_images_by_link(breed, link, image_width_requir, img_height_requir,
                            watermark, watermark_opacity, app_media_root):

    # use header because some links raise 403 error
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
                         '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    req = Request(link, headers=hdr)
    image_on_web = urlopen(req)
    image_buffer = image_on_web.read()
    #  load raw data into a BytesIO container
    image_buffer_byte = BytesIO(image_buffer)
    image_buffer_edited = img_resizer_and_watermark_add(image_buffer_byte, image_width_requir,
                                                        img_height_requir, watermark,
                                                        watermark_opacity)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_img_filename = timestamp + '.png'
    # path that will be written in objects attribute .image
    upload_to_new_img_filename = os.path.join('uploads/product', breed, new_img_filename)
    image_buffer_edited.save(os.path.join(app_media_root, upload_to_new_img_filename), 'PNG')
    image_on_web.close()
    return upload_to_new_img_filename


def main():
    breeds_list, links = parser_breeds()
    breeds_list = breeds_list[61:160]
    links = links[61:160]
    description = breeds_links_read(links)
    for i, breed in enumerate(breeds_list):
        print('Start downloading images for ' + breed)
        links = request_to_google_cse(API_KEY, breed, CUSTOM_SEARCH_ENGINE_ID, NUMBER_IMG_REQUIR)
        folder_single_breed_img = os.path.join(MEDIA_ROOT, 'uploads/product', breed)

        # create folder for each breed if it isn't exist
        if not os.path.exists(folder_single_breed_img):
            os.makedirs(folder_single_breed_img)

        new_dog_product = Product(available=True, title=breed, content=description[i])
        new_dog_product.save()
        variation = ProductVariation(product=new_dog_product, default=True,
                                     unit_price=choice(PRICE_CHOICES), sale_from=timezone.now())
        variation.save()
        for link in links['items']:
            try:
                img_resized = download_images_by_link(breed, link['link'], IMG_WIDTH_REQUIR, IMG_HEIGHT_REQUIR,
                                                      os.path.join(MEDIA_ROOT, WATERMARK), WATERMARK_OPACITY,
                                                      MEDIA_ROOT)
                # create a new instance of ProductImage class and link it with Product class
                image = ProductImage(product=new_dog_product)

                # assign path to image to ProductImage instance
                image.file = img_resized
                image.save()
                print(img_resized + ' was downloaded')
            except HTTPError:
                print('HTTP Error 403: Forbidden. Link is not valid')
            except OSError:
                print('OSError.')

        # Set the first instance of ProductImage as default image for default variation
        new_dog_product.variations.set_default_images([])

        # Copy duplicate fields (``Priced`` fields) from the default variation to the product.
        new_dog_product.copy_default_variation()



if __name__ == '__main__':
     main()
