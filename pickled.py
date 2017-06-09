#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: pickled.py
# Author: Yahui Liu <yahui.cvrs@gmail.com>; Try <trywen@qq.com>

import os
import pickle, cPickle
import cv2
import numpy as np

BIN_COUNTS = 5





def pickled(savepath, data, label, fnames, bin_num=BIN_COUNTS, mode="train"):
  '''
    savepath (str): save path
    data (array): image data, a nx3072 array
    label (list): image label, a list with length n
    fnames (str list): image names, a list with length n
    bin_num (int): save data in several files
    mode (str): {'train', 'test'}
  '''
  assert os.path.isdir(savepath)
  total_num = len(fnames)
  samples_per_bin = total_num / bin_num
  assert samples_per_bin > 0
  idx = 0
  for i in range(bin_num): 
    start = i*samples_per_bin
    end = (i+1)*samples_per_bin
    if end <= total_num and i+1 < bin_num:
      dict = {'data': data[start:end, :],
              'labels': label[start:end],
              'filenames': fnames[start:end]}
    else:
      dict = {'data': data[start:, :],
              'labels': label[start:],
              'filenames': fnames[start:]}
    
    savename = ""
    if mode == "train":
      dict['batch_label'] = "training batch {} of {}".format(idx, bin_num)
      savename = 'data_batch_'+str(idx)
    else:
      dict['batch_label'] = "testing batch {} of {}".format(idx, bin_num)
      savename = 'test_batch'
      
    with open(os.path.join(savepath, savename), 'wb') as fi:
      cPickle.dump(dict, fi)
    idx = idx + 1

def unpickled(filename):
  assert os.path.isdir(filename)
  with open(filename, 'rb') as fo:
    dict = cPickle.load(fo)
  return dict


def imread(im_path, shape=None, color="RGB", mode=cv2.IMREAD_UNCHANGED):
  im = cv2.imread(im_path, cv2.IMREAD_UNCHANGED)
  if color == "RGB":
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    # im = np.transpose(im, [2, 1, 0])
  if shape != None:
    assert isinstance(shape[0], int) 
    assert isinstance(shape[1], int) 
    im = cv2.resize(im, (shape[1], shape[0]))
  return im

#read data with images list file
def read_data(filename, data_path, shape=[32,32], color='RGB'):
  """
     filename (str): a file 
       data file is stored in such format:
         image_name  label
     data_path (str): image data folder
     return (numpy): a array of image and a array of label
  """ 
  if os.path.isdir(filename):
    print "Can't found data file!"
  else:
    f = open(filename)
    lines = f.read().splitlines()
    count = len(lines)
    data = np.zeros((count, shape[0] * shape[1] * 3), dtype=np.uint8)
    #label = np.zeros(count, dtype=np.uint8)
    lst = [ln.split(' ')[0] for ln in lines]
    label = [int(ln.split(' ')[1]) for ln in lines]
    
    idx = 0
    #s, c = SHAPE, CHANNEL_LEN
    c = shape[0] * shape[1]
    for ln in lines:
      fname, lab = ln.split(' ')
      im = imread(os.path.join(data_path, fname), shape=shape, color='RGB')
      '''
      im = cv2.imread(os.path.join(data_path, fname), cv2.IMREAD_UNCHANGED)
      im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
      im = cv2.resize(im, (s, s))
      '''
      data[idx,:c] =  np.reshape(im[:,:,0], c)
      data[idx, c:2*c] = np.reshape(im[:,:,1], c)
      data[idx, 2*c:] = np.reshape(im[:,:,2], c)
      
      label[idx] = int(lab)
      idx = idx + 1
      
    return data, label, lst



def build_meta(data_path, save_path):
  with open(save_path+"/batches.meta", 'a+') as f:
    f.truncate()
    for label in os.listdir(data_path):
      if os.path.isdir(data_path+"/"+label):
        f.write(label+"\n")

def build_filelist(data_path, filename):
  labelidx = 0
  with open(filename, 'a+') as f:
      f.truncate()
      for label in os.listdir(data_path):
        labeldir = data_path+"/"+label
        if os.path.isdir(labeldir):
          files = []
          _listfiles(labeldir, files)
          for filename in files:
            f.write("{} {}\n".format(filename[len(data_path)+1:], labelidx))
          labelidx += 1
    
def _listfiles(path, files):
  for name in os.listdir(path):
    filename = path+"/"+name
    if os.path.isdir(filename):
      _listfiles(filename, files)
    if os.path.isfile(filename):
      files.append(filename)
        
        
        
        
    