from utils import ImageUtils
from segment import Segment
from group import Group

from scipy import ndimage
from scipy.misc import imsave
import numpy as np


class ImageHandler:
    def __init__(self, image_name):
        self.image_name = image_name
        self.utils = ImageUtils()

        self.colors = []
        self.backgroundColor = -1
        self.noises = []

        self.foregroundSize = 0
        self.backgroundSize = 0
        self.max_group_size = 0

        self.groups = []

    def set_up(self):
        self.im = self.utils.read_image(self.image_name)
        self.filtered_image = self.utils.image_filter(self.im)

    def find_components(self):
        colors = np.lib.arraysetops.unique(self.filtered_image)
        self.colors = []

        for color in colors:
            im_color = (self.filtered_image == color)
            count = sum(sum(im_color))

            if count > 0.0005 * self.im.size:
                if count > self.backgroundSize:
                    if self.backgroundColor != -1:
                        self.colors.append(self.backgroundColor)
                        self.foregroundSize += self.backgroundSize
                        self.max_group_size = max(self.max_group_size, self.backgroundSize)

                    self.backgroundSize  = count
                    self.backgroundColor = color
                    continue

                self.max_group_size = max(self.max_group_size, count)
                self.foregroundSize += count
                self.colors.append(color)
            else:
                self.noises.append(color)

    def create_groups(self):
        groups = [[self.backgroundColor, 'background']]
        [groups.append([i, 'foreground']) for i in self.colors]
        [groups.append([i, 'noise']) for i in self.noises]

        size_data = []

        for group_color, group_label in groups:
            gr = Group(self.filtered_image == group_color, group_label)
            gr.find_components()
            data = gr.get_segments()
            data['relative_sizes'] = [gr.area/self.foregroundSize, gr.area/self.max_group_size]

            size_data.append(data)

        return size_data

