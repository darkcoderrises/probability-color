import numpy as np
from scipy.misc import imread
from scipy import stats

class ImageUtils(object):
    def read_image_color(self, image_name):
        return imread(image_name, mode='RGB')

    def read_image(self, image_name):
        return imread(image_name, mode='L')

    def image_filter(self, im):
        n = 8
        im_pad = np.pad(im, n/2, 'edge')

        lenX, lenY = im.shape
        filter_image = np.zeros(im.shape, dtype=np.int)

        for i in xrange(lenX):
            for j in xrange(lenY):
                pad = im_pad[i:(i+n), j:(j+n)]
                mode = stats.mode(pad, axis=None)
                filter_image[i][j] = mode[0][0]

        return filter_image

