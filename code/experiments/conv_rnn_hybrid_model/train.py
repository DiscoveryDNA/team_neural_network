import torch
import time
import os
import pickle
import logging
from absl import app, flags
from time import gmtime, strftime

FLAGS = flags.FLAGS

flags.DEFINE_integer('N', 500, 'number of images')