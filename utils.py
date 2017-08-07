import numpy as np
from scipy.misc import imread
from scipy import stats
from collections import Counter

import warnings

def check_group_collide(gr1, gr2):
    return sum(sum(gr1.dilated_image * gr2.dilated_image)) > 0

def flatten_segment(data):
    data = data.flatten()
    return [data[0], data[1], data[3]]

def binize_colors(data):
    binize_data = {}
    for key in data.keys():
        binize_data[key] = int(10*round(data[key]/100, 1))

    return binize_data

def prepare_group(group):
    flatten_group = [group['number_of_segments']]
    flatten_group.extend(group['relative_sizes'])
    flatten_group.extend(flatten_segment(group['segment_spread']))
    flatten_group.extend(group['segment_sizes'])

    return flatten_group


class ColorUtils(object):
    @staticmethod
    def chromatic_difference(l, a, b):
        return float(a**2 + b**2) / (l**2 + a**2 + b**2 + 0.001)

    @staticmethod
    def saturation(l,a,b):
        return  float(a**2 + b**2) / (l**2 + a**2 + b**2 + 0.001) ** 0.5

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
                mode = Counter(pad.flatten()).most_common(1)
                filter_image[i][j] = mode[0][0]

        return filter_image

    @staticmethod
    def prepare_group_data(data):
        size_data, color_data = data

        for i, value in enumerate(color_data):
            color = value
            group = size_data[i]

            yield prepare_group(group), binize_colors(color)


    @staticmethod
    def prepare_segment_data(data):
        size_data, color_data = data

        for i, value in enumerate(color_data):
            color = value
            group = size_data[i]

            for segment in group["each_segment_data"]:
                flatten_segment = []
                for key in segment.keys():
                    if key=="area":
                        continue

                    if type(segment[key]) == list:
                        flatten_segment.extend(segment[key])
                    else:
                        flatten_segment.append(segment[key])

                yield flatten_segment, binize_colors(color)

