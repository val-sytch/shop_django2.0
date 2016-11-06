import configparser
import os

path = os.path.realpath(os.path.dirname(__file__))
config = configparser.ConfigParser(interpolation=None)
file_config = 'config{0}.ini'.format("_" + os.environ.get('DJANGO_PROJ_MODE')
                                     if os.environ.get('DJANGO_PROJ_MODE') else '')
config.read(os.path.join(path, file_config))

# APP_DIR = path.rsplit('/djog', 1)[0]

WATERMARK = config.get('PATH', 'watermark')

IMG_WIDTH_REQUIR = int(config.get('IMAGES', 'width'))
IMG_HEIGHT_REQUIR = int(config.get('IMAGES', 'height'))
WATERMARK_OPACITY = float(config.get('IMAGES', 'watermark_opacity'))
NUMBER_IMG_REQUIR = int(config.get('IMAGES', 'numb_img_requir'))

ALLOWED_EXTENSIONS = ['jpg','jpeg','gif','png']
