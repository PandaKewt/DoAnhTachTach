from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count
from PIL import Image, ImageOps
from threading import Thread, enumerate
from os import path, mkdir
from glob import glob
import time
import sys


# UI
from tkinter import Tk, filedialog, BooleanVar, StringVar, DoubleVar, messagebox, mainloop, END
from tkinter.ttk import Label, Button, Progressbar, Checkbutton, Frame, Entry
# import tkinter as tk

opacity = 90
scale = 16
tachTachOffset = (20, 10)
schoolOffset = (40, 80)

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

totalImage = 0
imageComplete = 0
onClose = False


def updateProgressBar():
    if totalImage == 0:
        pb['value'] = 0
    else:
        pb['value'] = imageComplete / totalImage * 100
    root.after(100, updateProgressBar)


def callback(_):
    global imageComplete
    imageComplete += 1
    if (imageComplete == totalImage):
        timeToRun.set(time.time() - start_time)
        pool.close()


def imageProcessing(imgPath):
    img = Image.open(imgPath, 'r')
    img = ImageOps.exif_transpose(img)

    if useResize:
        img.thumbnail((2048, 2048), Image.LANCZOS, 3)

    imgW, imgH = img.size
    if imgW > imgH:
        tachTachLogoSize = imgH * scale // 100
        schoolLogoSize = imgW * scale // 100
    else:
        tachTachLogoSize = imgW * scale // 100
        schoolLogoSize = imgH * scale // 100

    if useTachTachLogo:
        tachTachLogoImg = tachTachLogoImgOriginal
        tachTachLogoImg.thumbnail((tachTachLogoSize, tachTachLogoSize))
        img.paste(tachTachLogoImg, tachTachOffset, tachTachLogoImg)

    if useSchoolLogo:
        schoolLogo = schoolLogoOriginal
        schoolLogo.thumbnail((schoolLogoSize, schoolLogoSize))
        schoolLogoWidth, _ = schoolLogo.size
        img.paste(schoolLogo, (imgW - schoolLogoWidth -
                               schoolOffset[0], schoolOffset[1]), schoolLogo)

    img.save(dirAddr + '\\output\\' + path.basename(imgPath))


def startProcess(folder):
    global start_time
    start_time = time.time()
    global pool
    pool = Pool(cpu_count())
    if not path.exists(folder + '\\output'):
        mkdir(folder + '\\output')
    for imgPath in glob(folder + '/*.jpg'):
        pool.apply_async(imageProcessing, (imgPath,), callback=callback)


def fileDialog():
    global dirAddr
    global totalImage
    dirAddr = filedialog.askdirectory()
    pathAddr.set(dirAddr)
    pathEntry.xview("end")
    totalImage = len(glob(dirAddr + '/*.jpg'))


def start():
    if 'dirAddr' in globals():
        if len(enumerate()) == 1:
            global imageComplete
            global useTachTachLogo
            global useSchoolLogo
            global useResize

            imageComplete = 0
            useTachTachLogo = tachTachLogoEnable.get()
            useSchoolLogo = schoolLogoEnable.get()
            useResize = resizeEnable.get()

            if useSchoolLogo == False and useTachTachLogo == False:
                messagebox.showwarning(
                    title='Tạch Tạch Logo Insertion', message='Chưa lựa chọn chức năng')
                print('log')
                return
            else:
                Thread(target=startProcess, args=(dirAddr,)).start()
        else:
            messagebox.showwarning(
                title='Tạch Tạch Logo Insertion', message='Đang đổ ảnh, vui lòng thử lại sau ít phút')
    else:
        messagebox.showwarning(
            title='Tạch Tạch Logo Insertion', message='Chưa lựa chọn thư mục')


def onClosing():
    sys.exit()


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root = Tk()
    global schoolLogoEnable
    global tachTachLogoEnable
    global pathAddr
    global pathEntry

    pathAddr = StringVar()
    timeToRun = DoubleVar()
    resizeEnable = BooleanVar()
    schoolLogoEnable = BooleanVar()
    tachTachLogoEnable = BooleanVar()

    resizeEnable.set(False)
    schoolLogoEnable.set(True)
    tachTachLogoEnable.set(True)
    timeToRun.set(0)

    root.title('Tạch Tạch Logo Insertion')
    pathFrame = Frame(root)
    pathLabel = Label(pathFrame, text='Path')
    pathEntry = Entry(pathFrame, textvariable=pathAddr, state='disabled')

    pb = Progressbar(
        root,
        orient='horizontal',
        mode='determinate',
        length=200
    )

    timeFrame = Frame(root)
    timeLabel = Label(timeFrame, text='Time to run')
    timeEntry = Entry(timeFrame, textvariable=timeToRun, state='disabled')

    selectionFrame = Frame(root)
    schoolLogo = Checkbutton(
        selectionFrame,
        text='FPT Logo',
        variable=schoolLogoEnable,
        onvalue=True,
        offvalue=False
    )
    tachTachLogo = Checkbutton(
        selectionFrame,
        text='Tạch Tạch Logo',
        variable=tachTachLogoEnable,
        onvalue=True,
        offvalue=False
    )
    resize = Checkbutton(
        selectionFrame,
        text='Resize Facebook',
        variable=resizeEnable,
        onvalue=True,
        offvalue=False
    )

    actionFrame = Frame(root)
    selectFolder = Button(
        actionFrame,
        text='Select Folder',
        command=fileDialog
    )
    startBtn = Button(
        actionFrame,
        text='Start',
        command=start
    )

    pathFrame.grid(row=0, column=0, padx=0, pady=10)
    pb.grid(row=1, column=0, padx=30, pady=10)
    timeFrame.grid(row=2, column=0, padx=10, pady=10)
    selectionFrame.grid(row=3, column=0, padx=10, pady=10)
    actionFrame.grid(row=4, column=0, padx=10, pady=10)

    # Path Frame
    pathLabel.grid(row=0, column=0, padx=10, pady=0)
    pathEntry.grid(row=0, column=1, padx=10, pady=0)

    # Action Frame
    timeLabel.grid(row=0, column=0, padx=10, pady=0)
    timeEntry.grid(row=0, column=1, padx=10, pady=0)

    # Selection Frame
    schoolLogo.grid(row=0, column=0, padx=10, pady=0)
    tachTachLogo.grid(row=0, column=1, padx=10, pady=0)
    resize.grid(row=0, column=2, padx=10, pady=0)

    # Action Frame
    selectFolder.grid(row=0, column=0, padx=10, pady=0)
    startBtn.grid(row=0, column=1, padx=10, pady=0)

    root.after(100, updateProgressBar)
    root.protocol("WM_DELETE_WINDOW", onClosing)
    mainloop()
