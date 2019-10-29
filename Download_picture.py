import pixabay
import os
import requests
import shutil
import logging

logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = '14047325-cabf4fbcc6c44e3b610a601aa'

# image operations
pixabay_api = pixabay.Image(API_KEY)

# custom image search
n_pages = 5
image_list = []
for page in range(1, n_pages + 1):
    pixbay_responce = pixabay_api.search(q='cats dogs',
                                         image_type='photo',
                                         orientation='horizontal',
                                         safesearch='true',
                                         order='latest',
                                         per_page=5,
                                         page=page + 1)
    image_list.extend(pixbay_responce['hits'])

n_images = len(image_list)
logger.info('Got {:d} images to download'.format(n_images))

for (i, hit) in enumerate(image_list):
    logger.info('Downloading image {:d} out of {:d}'.format(i + 1, n_images))
    im_url = hit['largeImageURL']
    im_ext = im_url.split('.')[-1]
    im_name = os.path.join('raw_images', '{:06d}.'.format(i+1) + im_ext)
    try:
        r = requests.get(im_url, stream=True)
        if r.status_code == 200:
            with open(im_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        print('unable to retrieve: {}'.format(str(e)))
