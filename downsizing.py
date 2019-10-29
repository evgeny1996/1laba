import cv2
import os
import glob


def donwnsample_image_to_jpeg_bytes(im, factor = 2, jpeg_quality = 80):
    resized_im = cv2.resize(im, (0, 0), fx=factor, fy=factor)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
    result, encimg = cv2.imencode('.jpg', resized_im, encode_param)
    return encimg

def write_bytes(enc_im, filename):
    with open(filename, 'wb') as f:
        f.write(enc_im)

def get_images_in_folder(folder, extensions = ('jpg', 'png')):
    result = list()
    for extension in extensions:
        images = glob.glob(os.path.join(folder, '*.'+extension))
        result.extend(images)
    return result

def make_directories(folder, downsample_rates):
    directories = {}
    if not os.path.exists(folder):
        os.mkdir(folder)
    for rate in downsample_rates:
        path = os.path.join(folder, '{:03d}'.format(rate))
        if not os.path.exists(path):
            os.mkdir(path)
        directories[rate] = path
    return directories

if __name__ == '__main__':
    quality = 60
    downsample_rates = (2, 4, 8, 16, 32)
    images = get_images_in_folder('image')
    directories = make_directories('downsampled', downsample_rates)
    for image_path in images:
        image = cv2.imread(image_path)
        im_name = os.path.basename(image_path)
        for downsample_rate in downsample_rates:
            downsampled = donwnsample_image_to_jpeg_bytes(image, factor =1. / downsample_rate, jpeg_quality = quality)
            write_bytes(downsampled, os.path.join(directories[downsample_rate], im_name))
