import numpy as np
from scipy.misc import imread
from scipy import stats

def check_group_collide(gr1, gr2):
    return sum(sum(gr1.dilated_image * gr2.dilated_image)) > 0

class ColorUtils(object):
    @staticmethod
    def chromatic_difference(l, a, b):
        return float(a**2 + b**2) / (l**2 + a**2 + b**2)

    @staticmethod
    def saturation(l,a,b):
        return  float(a**2 + b**2) / (l**2 + a**2 + b**2) ** 0.5

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

