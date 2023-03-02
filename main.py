from multiprocessing.pool import ThreadPool as Pool
from os import path, mkdir, cpu_count
from glob import glob
from PIL import Image
from sys import argv
import time

opacity = 90
scale = 16
tachTachOffset = (20, 10)
schoolOffset = (40, 80)

start_time = time.time()
tachTachLogoImgOriginal = Image.open('./logoTachTach.png', 'r')
tachTachLogoImgOriginal = tachTachLogoImgOriginal.convert('RGBA')

tachTachLogoImgOriginalAlpha = tachTachLogoImgOriginal.copy()
tachTachLogoImgOriginalAlpha.putalpha(255 * opacity // 100)
tachTachLogoImgOriginalMask = tachTachLogoImgOriginal.convert('L')
tachTachLogoImgOriginal.paste(
    tachTachLogoImgOriginalAlpha, mask=tachTachLogoImgOriginal)

schoolLogoOriginal = Image.open('./logoSchool.png', 'r')
schoolLogoOriginal = schoolLogoOriginal.convert('RGBA')

schoolLogoOriginalAlpha = schoolLogoOriginal.copy()
schoolLogoOriginalAlpha.putalpha(255 * opacity // 100)
schoolLogoOriginalMask = schoolLogoOriginal.convert('L')
schoolLogoOriginal.paste(
    schoolLogoOriginalAlpha, mask=schoolLogoOriginal)


def imageProcessing(imgPath):
    tachTachLogoImg = tachTachLogoImgOriginal
    schoolLogo = schoolLogoOriginal
    img = Image.open(imgPath, 'r')
    imgW, imgH = img.size

    if imgW > imgH:
        tachTachLogoSize = imgH * scale // 100
        schoolLogoSize = imgW * scale // 100
    else:
        tachTachLogoSize = imgW * scale // 100
        schoolLogoSize = imgH * scale // 100

    tachTachLogoImg.thumbnail((tachTachLogoSize, tachTachLogoSize))
    schoolLogo.thumbnail((schoolLogoSize, schoolLogoSize))
    schoolLogoWidth, schoolLogoHeight = schoolLogo.size

    img.paste(tachTachLogoImg, tachTachOffset, tachTachLogoImg)
    img.paste(schoolLogo, (imgW - schoolLogoWidth -
              schoolOffset[0], schoolOffset[1]), schoolLogo)
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
