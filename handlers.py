from utils import ImageUtils
from utils import ColorUtils
from utils import check_group_collide
from utils import prepare_group
from segment import Segment
from group import Group

from scipy import ndimage
from scipy.misc import imsave
import numpy as np
from skimage import color
from itertools import combinations


class ImageHandler:
    def __init__(self, image_name):
        self.image_name = image_name
        self.utils = ImageUtils()

        self.colors = []
        self.backgroundColor = -1
        self.noises = []

        self.foregroundSize = 0.001
        self.backgroundSize = 0.001
        self.max_group_size = 0.001

        self.groups = []

    def set_up(self):
        self.color_im = color.rgb2lab(self.utils.read_image_color(self.image_name))
        self.im = self.utils.read_image(self.image_name)
        self.filtered_image = self.utils.image_filter(self.im)

    def find_components(self):
        colors = np.lib.arraysetops.unique(self.filtered_image)
        self.colors = []

        for color in colors:
            im_color = (self.filtered_image == color)
            count = sum(sum(im_color))
            self.max_group_size = max(self.max_group_size, count)

            if count > 0.0005 * self.im.size:
                if count > self.backgroundSize:
                    if self.backgroundColor != -1:
                        self.colors.append(self.backgroundColor)
                        self.foregroundSize += self.backgroundSize

                    self.backgroundSize  = count
                    self.backgroundColor = color
                    continue

                self.foregroundSize += count
                self.colors.append(color)
            else:
                self.noises.append(color)

    def create_groups(self):
        groups = [[self.backgroundColor, 0]]
        [groups.append([i, 1]) for i in self.colors]
        [groups.append([i, 2]) for i in self.noises]

        size_data = []
        color_data = []

        for group_color, group_label in groups:
            gr = Group(self.filtered_image == group_color, group_label)
            gr.find_components()
            data = gr.get_segments()
            data['relative_sizes'] = [gr.area/self.foregroundSize, gr.area/self.max_group_size]
            size_data.append(data)

            indexes = np.where(gr.im)
            l, a, b = self.color_im[indexes[0][0], indexes[1][0], :]
            gr.set_lab(l,a,b)

            color_data.append({
                'lightness': l,
                'saturation': gr.get_saturation(),
            })

            gr.dilate()
            self.groups.append(gr)

        self.groups.sort(key=lambda x: x.area, reverse=True)
        return size_data, color_data

    def create_pairwise(self):

        for gr1, gr2 in combinations(self.groups, 2):
            if not check_group_collide(gr1, gr2):
                continue

            dilate = lambda gr: ndimage.binary_dilation(gr.dilated_image)
            enclosure = lambda gr1, gr2: sum(sum(dilate(gr1) * gr2.im)) / float(sum(sum(dilate(gr1) - gr1.im)))

            pairwise_data = {
                'perceptual_distance': np.linalg.norm(gr1.get_lab() - gr2.get_lab())/100,
                'relative_lightness': np.absolute(gr1.get_lightness() - gr2.get_lightness())/100,
                'relative_saturation': np.absolute(gr1.get_saturation() - gr2.get_saturation())/100,
                'chromatic_difference': ColorUtils.chromatic_difference(*(gr1.get_lab() - gr2.get_lab()))
            }

            for i in pairwise_data.keys():
                pairwise_data[i] = int(10*round(pairwise_data[i], 1))

            yield prepare_group(gr1.memory) + [enclosure(gr1, gr2)] + prepare_group(gr2.memory) + [enclosure(gr2, gr1)], pairwise_data

    def create_compatibility(self):
        num_groups = len(self.groups)
        colors = []

        for i in range(5):
            colors.append(self.groups[i%num_groups].get_lab())

        return colors

