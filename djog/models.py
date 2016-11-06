from __future__ import unicode_literals

import os
from datetime import datetime
from django.dispatch import receiver
from filebrowser_safe.views import filebrowser_post_upload
from services.img_resizer_and_watermark_add import img_resizer_and_watermark_add
from configs.config import (IMG_WIDTH_REQUIR, IMG_HEIGHT_REQUIR,
                            WATERMARK, WATERMARK_OPACITY, ALLOWED_EXTENSIONS)
from djog.settings import MEDIA_ROOT



@receiver(filebrowser_post_upload)
def img_resizer_watermarker(sender, file, **kwargs):
    if str(file).rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        image_uploaded = os.path.join(MEDIA_ROOT, str(file))
        # open uploaded image, resize it and put watermark
        resized_img_with_watermark = img_resizer_and_watermark_add(image_uploaded, IMG_WIDTH_REQUIR, IMG_HEIGHT_REQUIR,
                                                                   os.path.join(MEDIA_ROOT, WATERMARK), WATERMARK_OPACITY)
        # save edited image near uploaded image with the new filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        image_renamed = str(file).rsplit('/', 1)[0] + '/' + timestamp + '.png'
        abs_image_renamed = os.path.join(MEDIA_ROOT, image_renamed)
        resized_img_with_watermark.save(abs_image_renamed, 'PNG')
        # delete uploaded image
        os.remove(image_uploaded)
