# -*- coding:utf-8 -*-
__author__ = 'wangtao'
from PIL import Image
import os
import pytesseract

imgpath = r"E:\verifyims\source\rand.jpeg"

imgsavepath = r"E:\verifyims\dst_erzhihua\\" + os.path.basename(imgpath)

img = Image.open(imgpath)
img = img.convert("RGBA")

pixdata = img.load()

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x,y][0] < 90:
            pixdata[x,y] = (0,0,0,255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x,y][1] < 136:
            pixdata[x,y] = (0,0,0,255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x,y][2]>0:
            pixdata[x,y]=(255,255,255,255)

img.save(imgsavepath, "jpeg")

im_orig = Image.open(imgsavepath)
big = im_orig.resize((1000,500), Image.NEAREST)

authcode = str(pytesseract.image_to_string(Image.open(imgsavepath), lang='chi_sim'))
print authcode


