from multiprocessing.pool import ThreadPool as Pool
from os import path, mkdir, cpu_count
from glob import glob
from PIL import Image
from sys import argv
import time

opacity = 90
scale = 16
offset = (20, 20)

start_time = time.time()
tachTachLogoImgOriginal = Image.open('./logoTachTach.png', 'r')
tachTachLogoImgOriginal = tachTachLogoImgOriginal.convert('RGBA')

tachTachLogoImgOriginalAlpha = tachTachLogoImgOriginal.copy()
tachTachLogoImgOriginalAlpha.putalpha(255 * opacity // 100)
tachTachLogoImgOriginalMask = tachTachLogoImgOriginal.convert('L')
tachTachLogoImgOriginal.paste(
    tachTachLogoImgOriginalAlpha, mask=tachTachLogoImgOriginal)


def imageProcessing(imgPath):
    tachTachLogoImg = tachTachLogoImgOriginal
    img = Image.open(imgPath, 'r')
    imgW, imgH = img.size

    if imgW > imgH:
        tachTachLogoSize = imgH * scale // 100
    else:
        tachTachLogoSize = imgW * scale // 100

    tachTachLogoImg.thumbnail((tachTachLogoSize, tachTachLogoSize))

    img.paste(tachTachLogoImg, offset, tachTachLogoImg)
    img.save(argv[1] + '\\output\\' + path.basename(imgPath))


if path.exists(argv[1]):
    if not path.exists(argv[1] + '\\output'):
        mkdir(argv[1] + '\\output')
    pool = Pool(cpu_count())
    for imgPath in glob(argv[1] + '/*.jpg'):
        pool.apply_async(imageProcessing, (imgPath,))
    pool.close()
    pool.join()

print("--- %s seconds ---" % (time.time() - start_time))
