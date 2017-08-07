from handlers import ImageHandler
from utils import ImageUtils
import glob
import sys

if __name__ == "__main__":
    files = glob.glob('./color_lover/*.png')
    test_files = files[:10]
    train_files = files[10:100]

    for i in train_files:
        ih = ImageHandler(i)
        ih.set_up()
        ih.find_components()
        data = ih.create_groups()

        for size_data, color_data in ImageUtils.prepare_group_data(data):
            print size_data
