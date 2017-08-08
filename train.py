from handlers import ImageHandler
from utils import ImageUtils
import glob
import sys

import numpy as np
from sklearn.linear_model import LogisticRegression

import pickle

lightness = "lightness"
saturation = "saturation"

perceptual_distance = "perceptual_distance"
relative_lightness = "relative_lightness"
relative_saturation = "relative_saturation"
chromatic_difference = "chromatic_difference"

class Trainer(object):
    def __init__(self, keys=[lightness, saturation]):
        self.train_x = []

        self.train_y = {key: [] for key in keys}
        self.lr = {key: LogisticRegression() for key in keys}

    def add_x(self, data):
        self.train_x.append(data)

    def add_y(self, data):
        for key in data.keys():
            self.train_y[key].append(data[key])

    def add(self, data):
        size_data, color_data = data
        self.add_x(size_data)
        self.add_y(color_data)

    def train(self, key):
        self.lr[key].fit(self.train_x, self.train_y[key])

    def train_all(self):
        for key in self.train_y.keys():
            self.train(key)


if __name__ == "__main__":
    files = glob.glob('./color_lover/*.png')
    test_files = files[:100]
    train_files = files[1000:]

    group_trainer = Trainer()
    segment_trainer = Trainer()
    pairwise_trainer = Trainer([perceptual_distance, relative_lightness, relative_saturation, chromatic_difference])

    for i in train_files:
        try:
            ih = ImageHandler(i)
            ih.set_up()
            ih.find_components()
            data = ih.create_groups()

            map(group_trainer.add, ImageUtils.prepare_group_data(data))
            map(segment_trainer.add, ImageUtils.prepare_segment_data(data))
            map(pairwise_trainer.add, ih.create_pairwise())
        except:
            continue


    print "learning"
    group_trainer.train_all()
    segment_trainer.train_all()
    pairwise_trainer.train_all()

    with open('training_models.pkl', 'wb+') as fid:
        pickle.dump(group_trainer, fid)
        pickle.dump(segment_trainer, fid)
        pickle.dump(pairwise_trainer, fid)

