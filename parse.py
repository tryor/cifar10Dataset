# -*- coding:gbk -*-
import pickle as p
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as plimg
from PIL import Image

SHAPE = (3, 100, 100)

def load_CIFAR_batch(filename):
    """ load single batch of cifar """
    with open(filename, 'rb')as f:
        datadict = p.load(f)
        
        X = datadict['data']
        Y = datadict['labels']
        
        print X.shape
        X = X.reshape(X.shape[0], SHAPE[0], SHAPE[1], SHAPE[2])
        Y = np.array(Y)
        return X, Y

def load_CIFAR_Labels(filename):
    with open(filename, 'rb') as f:
        lines = [x for x in f.readlines()]
        print(lines)


if __name__ == "__main__":
    #load_CIFAR_Labels("bin/batches.meta")
    imgX, imgY = load_CIFAR_batch("bin/test_batch")
    print (imgX.shape)
    print ("���ڱ���ͼƬ:")
    for i in xrange(imgX.shape[0]):
        imgs = imgX[i - 1]
        if i < 100 :#ֻѭ��100��ͼƬ,���ע�͵����Ա��������е�ͼƬ,ͼƬ�϶�,����Ҫһ����ʱ��
            img0 = imgs[0]
            img1 = imgs[1]
            img2 = imgs[2]
            i0 = Image.fromarray(img0)
            i1 = Image.fromarray(img1)
            i2 = Image.fromarray(img2)
            img = Image.merge("RGB",(i0,i1,i2))
            name = "img" + str(i)+".png"
            img.save("data2/images/"+name,"png")#�ļ�������RGB�ںϺ��ͼ��
            for j in xrange(imgs.shape[0]):
                img = imgs[j - 1]
                name = "img" + str(i) + str(j) + ".png"
                print ("���ڱ���ͼƬ" + name)
                plimg.imsave("data2/image/" + name, img)#�ļ�������RGB�����ͼ��

    print ("�������.")