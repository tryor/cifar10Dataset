#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, cv2
from pickled import *

data_path = './data/train'
file_list = './data/train/images.lst'
save_path = './bin'

testing_data_path = './data/testing'
testing_file_list = './data/testing/images.lst'

if __name__ == '__main__':
    
  #Build training data
  build_filelist(data_path, file_list) 
  data, label, lst = read_data(file_list, data_path, shape=[32, 32])
  pickled(save_path, data, label, lst, bin_num = 2) 
  build_meta(data_path, save_path)
  
  #Build test data
  build_filelist(testing_data_path, testing_file_list)
  data, label, lst = read_data(testing_file_list, testing_data_path, shape=[32, 32])
  pickled(save_path, data, label, lst, bin_num = 1, mode="test")


