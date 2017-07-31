from segment import Segment
from utils import ColorUtils

import numpy as np
from scipy import ndimage

class Group(object):
    def __init__(self, im, label):
        self.im = im
        self.label = label
        self.segments = []
        self.area = 0

        self.max_seg_area = 0

    def dilate(self):
        self.dilated_image = ndimage.binary_dilation(self.im)

    def find_components(self):
        components, nr_objects = ndimage.label(self.im) 

        for component in xrange(1, nr_objects+1):
            segment_im = (components == component)
            segment = Segment(segment_im, self.label)
            segment.process()

            self.segments.append(segment)
            self.max_seg_area = max(self.max_seg_area, segment.area)
            self.area += segment.area

    def set_lab(self, l, a, b):
        self.lab = [l,a,b]

    def get_lab(self):
        return np.asarray(self.lab)

    def get_lightness(self):
        return self.lab[0]

    def get_saturation(self):
        return ColorUtils.saturation(*self.lab)

    def get_segments(self):
        segment_centers = []
        segment_sizes = []

        each_segment_data = []

        for segment in self.segments:
            segment_centers.append(segment.get_center())
            segment_sizes.append([segment.area, segment.xmin, segment.xmax, segment.ymin, segment.ymax])

            each_segment_data.append({
                'relative_sizes': [segment.area/self.area, segment.area/self.max_seg_area],
                'elongation': segment.get_elongation(),
                'centrality': segment.centrality(),
                'role_label': self.label,
                'area': segment.area
            })

        segment_spread = np.cov(segment_centers)
        number_of_segments = len(segment_sizes)

        return {
            'segment_spread': segment_spread,
            'each_segment_data': each_segment_data,
            'number_of_segments': number_of_segments,
            'area': self.area,
            'segment_sizes': segment_sizes
        }


