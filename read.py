#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cPickle,pickle

def unpickle(file):
  with open(file, 'rb') as fo:
    dict = pickle.load(fo)
    #dict = pickle.load(fo)
  return dict

if __name__ == '__main__':
  b = unpickle('./bin/data_batch_0')
  print "data.shape", b["data"].shape
  print "labels.size", len(b["labels"])
  #print "labels.size", (b["labels"])
  print "data[0]", b["data"][0:]
  
