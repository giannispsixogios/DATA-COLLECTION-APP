# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 23:21:26 2023

@author: giannisps
"""

import gdal
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import cm
from tkinter import filedialog
from skimage import draw
import rasterio as rs
from shapely.geometry import Polygon
import csv

# Open the TIFF file
ds = gdal.Open(r'C:\Users\GNR\Desktop\abeabe.tif')

# Get the number of bands
band_num = ds.RasterCount

# Select the bands for RGB display
r = ds.GetRasterBand(3).ReadAsArray().astype(float)
g = ds.GetRasterBand(2).ReadAsArray().astype(float)
b = ds.GetRasterBand(1).ReadAsArray().astype(float)

# Normalize the bands
r_norm = (r - np.min(r)) / (np.max(r) - np.min(r))
g_norm = (g - np.min(g)) / (np.max(g) - np.min(g))
b_norm = (b - np.min(b)) / (np.max(b) - np.min(b))

# Stack the bands
rgb = np.dstack((r_norm, g_norm, b_norm))


# Display the final image with valid colors
plt.imshow(rgb)
plt.show()


img = Image.fromarray(np.uint8((rgb)*255))

from tkinter import*

data = ds.ReadAsArray()


# img.save(r'C:\Users\GNR\Desktop\abeabe9900000.tif')




root = tk.Tk()
root.geometry("550x500")
root.title("DATA COLLECTION")


frame = tk.Frame(root, bg='#45aaf2')

lbl_pic_path = tk.Label(frame, text='Image Path:', padx=25, pady=25, font=('verdana',16), bg='#45aaf2')
lbl_show_pic = tk.Label(frame, bg='#45aaf2')
lbl_show_pic2 = tk.Label(frame, bg='#45aaf2')
entry_pic_path = tk.Entry(frame, font=('verdana', 16))

entry_pic_path = tk.Entry(frame, font=('verdana',16))
btn_browse = tk.Button(frame, text='Select Image',bg='grey', fg='#ffffff', font=('verdana',16))


def selectPic():
    global img
    global src
    global filename
    filename = filedialog.askopenfilename(initialdir="/images", title="Select Image", filetypes=((("All files", ".*"), ("TIFF files", ".tif"))))
    with rs.open(filename) as src:
        img = Image.fromarray(((src))).resize((100, 100))

    img = Image.open(filename).resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    lbl_show_pic['image'] = img
    entry_pic_path.insert(0, filename)
    
    
def displayPic():
    global img
    ndvi_tk = ImageTk.PhotoImage(img)
    lbl_show_pic2['image'] = ndvi_tk
    lbl_show_pic2.image = ndvi_tk
    




def record_click(event):
    x, y = event.x, event.y
    label = class_var.get()
    data.append((x, y, label))





#from tkinter import*



def save_data(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['x', 'y', 'label'])
        data = ds.ReadAsArray()
        for row in data:
            writer.writerow(row)
 
    
# Class selection
class_var = StringVar()
class_var.set('unlabeled')
classes = ['water', 'vegetation', 'soil', 'urban']
for c in classes:
     Radiobutton(root, text=c, variable=class_var, value=c).pack()

# Data storage
data = []
root.bind('<Button-1>', record_click)  



    
 
    
btn_browse.config(command=selectPic)
button1 = tk.Button(frame, text='Display image',bg='grey', fg='#ffffff', font=('verdana',16), command=displayPic)
Button = tk.Button(frame, text='Save',bg='grey', fg='#ffffff', font=('verdana',16), command=lambda: save_data('datumAS23.csv'))





frame.pack(expand=1)
lbl_pic_path.grid(row=0, column=0)
entry_pic_path.grid(row=0, column=1)
btn_browse.grid(row=0, column=2)
lbl_show_pic.grid(row=1, column=0, columnspan=3)
lbl_show_pic2.grid(row=3, column=0, columnspan=3)
button1.grid(row=2, column=0, columnspan=3)
Button.grid(row=1, column=1, columnspan=1)



#Button(root, text='Save', command=lambda: save_data('data.csv')).pack()



root.mainloop()








