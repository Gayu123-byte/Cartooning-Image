# This is a sample Python script.
import cv2_rgb #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
""" fileopenbox opens the box to choose file
and help us store file path as string """
def upload():
    ImagePath =easygui.fileopenbox()
    cartoonify(ImagePath)
def cartoonify(ImagePath):
    # read the image
    originalmage = cv2_rgb.imread(ImagePath)
    originalmage = cv2_rgb.cvtColor(originalmage, cv2_rgb.COLOR_BGR2RGB)
    # print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    ReSized1 = cv2_rgb.resize(originalmage, (960, 540))
    grayScaleImage = cv2_rgb.cvtColor(originalmage, cv2_rgb.COLOR_BGR2GRAY)
    ReSized2 = cv2_rgb.resize(grayScaleImage, (960, 540))
    smoothGrayScale = cv2_rgb.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2_rgb.resize(smoothGrayScale, (960, 540))
    getEdge = cv2_rgb.adaptiveThreshold(smoothGrayScale, 255,
                                    cv2_rgb.ADAPTIVE_THRESH_MEAN_C,
                                    cv2_rgb.THRESH_BINARY, 9, 9)
    ReSized4 = cv2_rgb.resize(getEdge, (960, 540))
    # applying bilateral filter to remove noise
    # and keep edge sharp as required
    colorImage = cv2_rgb.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2_rgb.resize(colorImage, (960, 540))
    # plt.imshow(ReSized5, cmap='gray')
    # masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2_rgb.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2_rgb.resize(cartoonImage, (960, 540))
    # plt.imshow(ReSized6, cmap='gray')
    # Plotting the whole transition
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()
def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname("C:/Users/priyanka/Desktop/ml")
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2_rgb.imwrite(path, cv2_rgb.cvtColor(ReSized6, cv2_rgb.COLOR_RGB2BGR))
    I = "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))
upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)
save1=Button(top,text="Save cartoon image",command=lambda: save(ImagePath="C:/Users/priyanka/Desktop/ml", ReSized6=""),padx=30,pady=5)
save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
save1.pack(side=TOP,pady=50)
top.mainloop()



