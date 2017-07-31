from utils import ImageUtils
from utils import ColorUtils
from utils import check_group_collide
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

        self.foregroundSize = 0
        self.backgroundSize = 0
        self.max_group_size = 0

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
        groups = [[self.backgroundColor, 'background']]
        [groups.append([i, 'foreground']) for i in self.colors]
        [groups.append([i, 'noise']) for i in self.noises]

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

        return size_data, color_data

    def create_pairwise(self):
        pairwise_data = []
        enclosure_strengths = 0.0

        for gr1, gr2 in combinations(self.groups, 2):
            if not check_group_collide(gr1, gr2):
                continue

            dilate = lambda gr: ndimage.binary_dilation(gr.dilated_image)
            e_strength = sum(sum(dilate(gr1) * dilate(gr2)))
            enclosure_strengths += e_strength

            pairwise_data.append({
                'color1': gr1.get_lab(),
                'color2': gr2.get_lab(),
                'enclosure_strength': e_strength,
                'perceptual_distance': np.linalg.norm(gr1.get_lab() - gr2.get_lab()),
                'relative_lightness': np.absolute(gr1.get_lightness() - gr2.get_lightness()),
                'relative_saturation': np.absolute(gr1.get_saturation() - gr2.get_saturation()),
                'chromatic_difference': ColorUtils.chromatic_difference(*(gr1.get_lab() - gr2.get_lab()))
            })

        return map(lambda d : d.update({'enclosure_strength': d['enclosure_strength']/enclosure_strengths}) or d, pairwise_data)

    def create_compatibility(self):
        pass

