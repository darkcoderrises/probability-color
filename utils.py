import numpy as np
from scipy.ndimage import imread

class ImageUtils(object):

    def read_image(image_name):
        return imread(image_name)

    def image_filter(im):
        n = 8
        im_pad = np.pad(im, n/2, 'constant')

        lenX, lenY, channel = a.shape
        filter_image = np.zeros(im.shape)

        for ch in range(channel):
            for i in xrange(lenX - n/2):
                for j in xrange(lenY - n/2):
                    filter_image[i,j,ch] = mode(a[i:i+n,j:j+n,ch])
                    #TODO mode

        return filter_image

