#!/usr/bin/env python
__author__ = 'Horea Christian'

import numpy as np
import pandas as pd
from numpy.random import permutation, choice, sample
from os import path

# General parameters:
image_subdir = 'img/'

local_dir = path.dirname(path.realpath(__file__)) + '/'
image_dir = local_dir + image_subdir

image_lsit = psth.listdir(image_dir)
print image_list
