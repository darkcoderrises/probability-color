from utils import ImageUtils
from segment import Segment
from scipy import ndimage
from scipy.misc import imsave
import numpy as np

import matplotlib.pyplot as plt

class ImageHandler:
    def __init__(self, image_name):
        self.image_name = image_name
        self.utils = ImageUtils()

        self.colors = []
        self.foregroundColor = -1
        self.noises = []

    def set_up(self):
        self.im =   self.utils.read_image(self.image_name)
        self.filtered_image = self.utils.image_filter(self.im)

    def find_components(self):
        colors = np.lib.arraysetops.unique(self.filtered_image)
        self.colors = []

        for color in colors:
            im_color = (self.filtered_image == color)
            count = sum(sum(im_color))

            maxCount = -1

            if count > 0.05 * self.im.size:
                if count > maxCount:
                    if self.foregroundColor != -1:
                        self.colors.append(self.foregroundColor)

                    maxCount = count
                    self.foregroundColor = color
                    continue

                self.colors.append(color)
            else:
                self.noises.append(color)

