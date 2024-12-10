import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from tkinter import messagebox as mBox
from PIL import Image, ImageTk
import subprocess
import cv2
from pylab import *
from matplotlib import path
import matplotlib.cm as cm
from matplotlib.widgets import Slider
from tkinter import filedialog
import numpy as np
from matplotlib.image import imread
from scipy import ndimage as ndi

from skimage.feature import peak_local_max

from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data

import matplotlib.pyplot as plt
from matplotlib import cm

import tkinter.scrolledtext as tkst
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector
from collections import deque
import matplotlib.image as mpimg

### Functions
def OPEN():
    global Original_Image
    global Dimension_Number
    global Original_image_Size
    root1.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("jpeg files", "*.jpg"),("png files", "*.png"),
                                                ("tif files", "*.TIF"), ("all files", "*.*")))
    Original_Image = Image.open(root1.filename)
    Original_Image=np.array(Original_Image)
    Original_image_Size = np.shape(Original_Image)
    print(len(Original_image_Size))


    a1 = np.shape(Original_Image)
    a1 = str(a1)
    tk.Label(root1, text='Dimensions: ').place(x=0,y=0)
    v_dim = tk.StringVar(root1, value=a1)
    e = tk.Entry(root1, textvariable=v_dim)
    e.place(x=70, y=0)



    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    def RGB_Show():
        root2 = tk.Toplevel()
        root2.geometry('600x600')

        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        image = Original_Image
        image = Image.fromarray(image)
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(root2, image=photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=tk.BOTH, expand='YES')

        root2.mainloop()

    def ShowChoice():
        a = int(v1.get())
        root2 = tk.Toplevel()
        root2.geometry('600x600')

        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        image = Original_Image[:, :, a]
        image = Image.fromarray(image)
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(root2, image=photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=tk.BOTH, expand='YES')

        root2.mainloop()

    def ShowChoiceOneBand():
        root2 = tk.Toplevel()
        root2.geometry('600x600')

        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        image = Original_Image
        image = Image.fromarray(image)
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(root2, image=photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=tk.BOTH, expand='YES')

    tk.Label(root1, text="""Choose your favourite view:""", justify=tk.LEFT, padx=20).place(x=0,y=20)

    if len(Original_image_Size) > 2:
        v1 = tk.StringVar()
        v1.set("L")  # initialize
        z=20
        for val, Dimension_Number in enumerate(Dimension_Number):
            z=z+20
            b = tk.Radiobutton(root1, text=Dimension_Number, padx=20, variable=v1, value=val, command=ShowChoice)
            b.place(x=0,y=z)
        if Original_image_Size[2] == 3:
            RGB_btn = tk.Button(root1, bg='#000000', fg='#b7f731', text='   RGB   ', padx=20, bd='5', command=RGB_Show)
            RGB_btn.place(x=0,y=20+z)
    else:
        z=20
        b = tk.Radiobutton(root1, text="Band 1", padx=20, value=1, command=ShowChoiceOneBand)
        b.place(x=0,y=z+20)



def Tresholding():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def Tresholding1():
        if len(Original_image_Size) > 2:
            global imgT
            a_Tresholding = int(numberChosen1.get())
            imgT = Original_Image[:, :, a_Tresholding - 1]

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)


            ax2.set_title(" Histogram", fontsize=12, color="#333533")

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(imgT, cmap='gray')

            hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Tresholding)+"Histogram")



            ax2.axvline(x=0,label="Treshold", color='r')
            ax2.legend(loc='best')


            fig.canvas.draw_idle()

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time = Slider(ax1_value, 'Tresholding:', 0, 255, valinit=0,color='r')

            def update(val):
                ax2.cla()

                hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
                a_Tresholding = int(numberChosen1.get())
                ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Tresholding)+"Histogram")
                ax2.axvline(x=int(s_time.val),label="Treshold", color='r')


                img = Original_Image[:, :, a_Tresholding - 1]
                img = np.array(img)
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if img[i, j] > s_time.val:
                            img[i, j] = 255
                        else:
                            img[i, j] = 0
                img3 = img
                ax1.imshow(img3, cmap='gray')

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Tresholding Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', img3)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Tresholded Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)


                fig.canvas.draw_idle()

            s_time.on_changed(update)
        else:

            imgT = Original_Image

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_title(" Histogram", fontsize=12, color="#333533")

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(imgT, cmap='gray')

            hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")

            ax2.axvline(x=0, label="Treshold", color='r')
            ax2.legend(loc='best')

            fig.canvas.draw_idle()

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time = Slider(ax1_value, 'Tresholding:', 0, 255, valinit=0, color='r')

            def update(val):
                ax2.cla()

                hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])

                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")
                ax2.axvline(x=int(s_time.val), label="Treshold", color='r')

                img = Original_Image
                img = np.array(img)
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if img[i, j] > s_time.val:
                            img[i, j] = 255
                        else:
                            img[i, j] = 0
                img3 = img
                ax1.imshow(img3, cmap='gray')

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Tresholding Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', img3)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Tresholded Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                fig.canvas.draw_idle()

            s_time.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Tresholding1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Tresholding1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()

# Code here
def Robertz():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def Robertz1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Robertz2():
                ax2.cla()

                kernel_3 = np.array([[-1, 0], [0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel() , color="gold", label="Band" + str(a_AverageFiltering) + "Histogram")


                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)


                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Robertz4():
                ax2.cla()

                kernel_3 = np.array([[0, -1], [1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter In X Direction   ', padx=20,
                             bd='1', command=Robertz2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter in Y direction   ', padx=20, bd='1',
                             command=Robertz4)
            btn3.place(x=720, y=650)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel() , color="gold", label="Band" + str(a_AverageFiltering) + "Histogram")
            ax2.legend(loc='best')


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Robertz2():
                ax2.cla()

                kernel_3 = np.array([[-1, 0], [0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Robertz4():
                ax2.cla()

                kernel_3 = np.array([[0, -1], [1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter In X Direction   ', padx=20,
                             bd='1', command=Robertz2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter in Y direction   ', padx=20, bd='1',
                             command=Robertz4)
            btn3.place(x=720, y=650)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold", label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBRobertz():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Robertz2():
                    ax2.cla()
                    kernel_3 = np.array([[-1, 0], [0, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')

                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Robertz4():
                    ax2.cla()

                    kernel_3 = np.array([[0, -1], [1, 0]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()


                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter In X Direction   ', padx=20,
                                 bd='1', command=Robertz2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter in Y direction   ', padx=20, bd='1',
                                 command=Robertz4)
                btn3.place(x=720, y=650)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBRobertz)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Robertz1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Robertz1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')


    root8.mainloop()


def Prewitt():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def Prewitt1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Prewitt2():
                ax2.cla()
                kernel_3 = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt4():
                ax2.cla()
                kernel_3 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt5():
                ax2.cla()
                kernel_3 = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt6():
                ax2.cla()
                kernel_3 = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Prewitt2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Prewitt4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Prewitt5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Prewitt6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Prewitt2():
                ax2.cla()
                kernel_3 = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt4():
                ax2.cla()
                kernel_3 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt5():
                ax2.cla()
                kernel_3 = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt6():
                ax2.cla()
                kernel_3 = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Prewitt2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Prewitt4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Prewitt5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Prewitt6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBPrewitt():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)


                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Prewitt2():
                    ax2.cla()
                    kernel_3 = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Prewitt4():
                    ax2.cla()
                    kernel_3 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Prewitt5():
                    ax2.cla()
                    kernel_3 = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Prewitt6():
                    ax2.cla()
                    kernel_3 = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                                 command=Prewitt2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                                 command=Prewitt4)
                btn3.place(x=630, y=650)
                btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1',
                                  command=Prewitt5)
                btn21.place(x=530, y=700)
                btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1',
                                  command=Prewitt6)
                btn31.place(x=630, y=700)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBPrewitt)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Prewitt1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Prewitt1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


    def Sobel():
        root8 = tk.Toplevel()
        root8.geometry("1800x900")
        root8.configure(background='white')
        root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")


        def Sobel1():
            if len(Original_image_Size) > 2:
                a_AverageFiltering = int(numberChosen1.get())
                img = Original_Image[:, :, a_AverageFiltering - 1]
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)


                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Sobel2():
                    ax2.cla()

                    kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(a_AverageFiltering) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel4():
                    ax2.cla()

                    kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(a_AverageFiltering) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel5():
                    ax2.cla()

                    kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(a_AverageFiltering) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel6():
                    ax2.cla()

                    kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(a_AverageFiltering) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                                command=Sobel2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                                command=Sobel4)
                btn3.place(x=630, y=650)
                btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Sobel5)
                btn21.place(x=530, y=700)
                btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Sobel6)
                btn31.place(x=630, y=700)

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                        label="Band" + str(a_AverageFiltering) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()


            else:
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Sobel2():
                    ax2.cla()

                    kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(1) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel4():
                    ax2.cla()

                    kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(1) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel5():
                    ax2.cla()

                    kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(1) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel6():
                    ax2.cla()

                    kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img.ravel(), color="gold",
                            label="Band" + str(1) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                    bd='5',
                                    command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                                command=Sobel2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                                command=Sobel4)
                btn3.place(x=630, y=650)
                btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Sobel5)
                btn21.place(x=530, y=700)
                btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Sobel6)
                btn31.place(x=630, y=700)

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                        label="Band" + str(1) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

        if len(Original_image_Size) > 2:
            Dimension_Number = []
            Dimension_Number_int = []
            for x1 in range(Original_Image.shape[2]):
                Dimension_Number_int.append(x1 + 1)
                Dimension_Number.append(("Band ", x1 + 1))

        else:
            Dimension_Number = [("Band", 1)]

        if len(Original_image_Size) > 2:
            ttk.Label(root8, text="Choose a band:").pack(anchor='w')
            number1 = tk.StringVar()
            numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
            numberChosen1['values'] = (Dimension_Number_int)
            numberChosen1.pack(anchor='w')
            numberChosen1.current(0)
            if len(Original_image_Size) == 3:
                def RGBSobel():
                    img = Original_Image
                    fig = plt.Figure(figsize=(13, 7))
                    canvas = FigureCanvasTkAgg(fig, root8)
                    canvas.get_tk_widget().place(x=200, y=0)

                    ax1 = fig.add_subplot(121)
                    ax2 = fig.add_subplot(122)

                    ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                    ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                    ax2.set_facecolor("#2E2E2E")

                    ax1.set_title("Original Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    toolbarFrame = tk.Frame(master=root8)
                    toolbarFrame.place(x=1000, y=650)

                    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                    toolbar.update()

                    def on_key_press(event):
                        print("you pressed {}".format(event.key))
                        key_press_handler(event, canvas, toolbar)

                    canvas.mpl_connect("key_press_event", on_key_press)

                    fig.subplots_adjust(bottom=0.25)

                    ax1.imshow(img, cmap='gray')

                    def Sobel2():
                        ax2.cla()

                        kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                        q = cv2.filter2D(img, -1, kernel_3)
                        ax1.imshow(q, cmap='gray')
                        hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                        hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                        hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                        hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                        def SaveI():
                            f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                            if f is None:
                                return

                            filename = f.name

                            cv2.imwrite(str(filename) + '.jpg', q)
                            f.close()

                        btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                        bd='5',
                                        command=SaveI)
                        btnw.place(x=400, y=0)

                        ax2.legend(loc='best')
                        fig.canvas.draw_idle()

                    def Sobel4():
                        ax2.cla()

                        kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                        q = cv2.filter2D(img, -1, kernel_3)
                        ax1.imshow(q, cmap='gray')
                        hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                        hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                        hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                        hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                        def SaveI():
                            f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                            if f is None:
                                return

                            filename = f.name

                            cv2.imwrite(str(filename) + '.jpg', q)
                            f.close()

                        btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                        bd='5',
                                        command=SaveI)
                        btnw.place(x=400, y=0)

                        ax2.legend(loc='best')
                        fig.canvas.draw_idle()

                    def Sobel5():
                        ax2.cla()

                        kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                        q = cv2.filter2D(img, -1, kernel_3)
                        ax1.imshow(q, cmap='gray')
                        hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                        hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                        hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                        hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                        def SaveI():
                            f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                            if f is None:
                                return

                            filename = f.name

                            cv2.imwrite(str(filename) + '.jpg', q)
                            f.close()

                        btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                        bd='5',
                                        command=SaveI)
                        btnw.place(x=400, y=0)

                        ax2.legend(loc='best')
                        fig.canvas.draw_idle()

                    def Sobel6():
                        ax2.cla()

                        kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                        q = cv2.filter2D(img, -1, kernel_3)
                        ax1.imshow(q, cmap='gray')
                        hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                        hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                        hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                        ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                        hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                        ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                        def SaveI():
                            f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                            if f is None:
                                return

                            filename = f.name

                            cv2.imwrite(str(filename) + '.jpg', q)
                            f.close()

                        btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                        bd='5',
                                        command=SaveI)
                        btnw.place(x=400, y=0)

                        ax2.legend(loc='best')
                        fig.canvas.draw_idle()

                    btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                                    command=Sobel2)
                    btn2.place(x=530, y=650)
                    btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                                    command=Sobel4)
                    btn3.place(x=630, y=650)
                    btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1',
                                    command=Sobel5)
                    btn21.place(x=530, y=700)
                    btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1',
                                    command=Sobel6)
                    btn31.place(x=630, y=700)

                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                                command=RGBSobel)
                btn.pack(anchor='w')
            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                            command=Sobel1)
            btn.pack(anchor='w')

        else:
            tk.Label(root8, text="Choose a band:").pack(anchor='w')
            number1 = tk.StringVar()
            numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
            numberChosen1['values'] = "1"
            numberChosen1.pack(anchor='w')
            numberChosen1.current(0)
            btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                            command=Sobel1)
            btn1.pack(anchor='w')


        def Quit():
            root8.quit()
            root8.destroy()

        button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                        bd='5', command=Quit)
        button.pack(anchor='w')

        root8.mainloop()

def Sobel():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def Sobel1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Sobel2():
                ax2.cla()

                kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel4():
                ax2.cla()

                kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel5():
                ax2.cla()

                kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel6():
                ax2.cla()

                kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Sobel2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Sobel4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Sobel5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Sobel6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(a_AverageFiltering) + "Histogram")

            ax2.legend(loc='best')
            fig.canvas.draw_idle()


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Sobel2():
                ax2.cla()

                kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel4():
                ax2.cla()

                kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel5():
                ax2.cla()

                kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel6():
                ax2.cla()

                kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Sobel2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Sobel4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Sobel5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Sobel6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(1) + "Histogram")

            ax2.legend(loc='best')
            fig.canvas.draw_idle()

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBSobel():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Sobel2():
                    ax2.cla()

                    kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel4():
                    ax2.cla()

                    kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel5():
                    ax2.cla()

                    kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel6():
                    ax2.cla()

                    kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                                 command=Sobel2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                                 command=Sobel4)
                btn3.place(x=630, y=650)
                btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1',
                                  command=Sobel5)
                btn21.place(x=530, y=700)
                btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1',
                                  command=Sobel6)
                btn31.place(x=630, y=700)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBSobel)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Sobel1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Sobel1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()

def USM():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def USM1():
        if len(Original_image_Size) > 2:
            a_USM = int(numberChosen1.get())
            img = Original_Image[:, :, a_USM - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.04, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.08, 0.78, 0.03])
            ax3_value = fig.add_axes([0.12, 0.12, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'K', 0, 30, valinit=0,color='r')
            s_time2 = Slider(ax2_value, 'Sigma X', 0, 30, valinit=0,color='g')
            s_time3 = Slider(ax3_value, 'Sigma Y', 0, 30, valinit=0,color='b')

            def USM3():
                global t1
                t1 = int(E1.get())

            def USM2(val):
                ax2.cla()
                b = cv2.GaussianBlur(img, (t1, t1), s_time2.val, s_time3.val)
                K = int(s_time1.val)
                gmask = img - b
                q = img + K * gmask
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_USM) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Kernel Size(odd number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=320, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=480, y=720)

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1', command=USM3)
            btn2.place(x=630, y=720)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(a_USM) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

            s_time1.on_changed(USM2)
            s_time2.on_changed(USM2)
            s_time3.on_changed(USM2)


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.04, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.08, 0.78, 0.03])
            ax3_value = fig.add_axes([0.12, 0.12, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'K', 0, 30, valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Sigma X', 0, 30, valinit=0, color='g')
            s_time3 = Slider(ax3_value, 'Sigma Y', 0, 30, valinit=0, color='b')

            def USM3():
                global t1
                t1 = int(E1.get())

            def USM2(val):
                ax2.cla()
                b = cv2.GaussianBlur(img, (t1, t1), s_time2.val, s_time3.val)
                K = int(s_time1.val)
                gmask = img - b
                q = img + K * gmask
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Kernel Size(odd number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=320, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=480, y=720)

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1', command=USM3)
            btn2.place(x=630, y=720)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

            s_time1.on_changed(USM2)
            s_time2.on_changed(USM2)
            s_time3.on_changed(USM2)

    if len(np.shape(Original_Image)) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBUSM():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=720)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)


                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.04, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.08, 0.78, 0.03])
                ax3_value = fig.add_axes([0.12, 0.12, 0.78, 0.03])
                s_time1 = Slider(ax1_value, 'K', 0, 30, valinit=0, color='r')
                s_time2 = Slider(ax2_value, 'Sigma X', 0, 30, valinit=0, color='g')
                s_time3 = Slider(ax3_value, 'Sigma Y', 0, 30, valinit=0, color='b')

                def USM3():
                    global t1
                    t1 = int(E1.get())

                def USM2(val):
                    ax2.cla()
                    b = cv2.GaussianBlur(img, (t1, t1), s_time2.val, s_time3.val)
                    K = int(s_time1.val)
                    gmask = img - b
                    q = img + K * gmask
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                L1 = tk.Label(root8, text="Kernel Size(odd number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=320, y=720)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=480, y=720)

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1', command=USM3)
                btn2.place(x=630, y=720)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

                s_time1.on_changed(USM2)
                s_time2.on_changed(USM2)
                s_time3.on_changed(USM2)

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBUSM)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=USM1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=USM1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def SAP():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")


    def SAP1():
        if len(Original_image_Size) > 2:
            a_SAP = int(numberChosen1.get())
            img = Original_Image[:, :, a_SAP - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)



            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img,cmap='gray')


            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Salt:', 0, 1, valinit=0,color='r')

            channel_2 = np.atleast_1d(img)
            noisy = np.zeros_like(channel_2)

            def update(val):

                s_and_p = np.random.rand(img.shape[0], img.shape[1])
                salt = s_and_p > s_time1.val
                pepper = s_and_p < 1 - s_time1.val
                for i in range(channel_2.shape[0] * channel_2.shape[1]):
                    if salt.ravel()[i] == 1:
                        noisy.ravel()[i] = 255
                    elif pepper.ravel()[i] == 1:
                        noisy.ravel()[i] = 0
                    else:
                        noisy.ravel()[i] = channel_2.ravel()[i]

                ax2.imshow(noisy, cmap='gray')

                S = s_time1.val
                P = 1 - s_time1.val
                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image(Salt="+str(S)+",Pepper="+str(P), fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Salt:', 0, 1, valinit=0, color='r')

            channel_2 = np.atleast_1d(img)
            noisy = np.zeros_like(channel_2)

            def update(val):

                s_and_p = np.random.rand(img.shape[0], img.shape[1])
                salt = s_and_p > s_time1.val
                pepper = s_and_p < 1 - s_time1.val
                for i in range(channel_2.shape[0] * channel_2.shape[1]):
                    if salt.ravel()[i] == 1:
                        noisy.ravel()[i] = 255
                    elif pepper.ravel()[i] == 1:
                        noisy.ravel()[i] = 0
                    else:
                        noisy.ravel()[i] = channel_2.ravel()[i]

                ax2.imshow(noisy, cmap='gray')

                S = s_time1.val
                P = 1 - s_time1.val
                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image(Salt=" + str(S) + ",Pepper=" + str(P), fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=SAP1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=SAP1)
        btn1.pack(anchor='w')





    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def GNoise():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def GNoise1():
        if len(Original_image_Size) > 2:
            a_GNoise = int(numberChosen1.get())
            img = Original_Image[:, :, a_GNoise - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Mean:', 0, 200, valinit=0,color='r')

            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])
            s_time2 = Slider(ax2_value, 'Sigma:', 0, 200, valinit=0,color='g')

            def update(val):

                gauss_noise = np.random.normal(s_time1.val, s_time2.val, (img.shape[0], img.shape[1]))

                g_noisy = img + gauss_noise

                ax2.imshow(g_noisy, cmap='gray')

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image", fontsize=12, color="#333533")


                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', g_noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)
            s_time2.on_changed(update)


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Mean:', 0, 200, valinit=0, color='r')

            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])
            s_time2 = Slider(ax2_value, 'Sigma:', 0, 200, valinit=0, color='g')

            def update(val):

                gauss_noise = np.random.normal(s_time1.val, s_time2.val, (img.shape[0], img.shape[1]))

                g_noisy = img + gauss_noise

                ax2.imshow(g_noisy, cmap='gray')

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', g_noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)
            s_time2.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=GNoise1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=GNoise1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()

#Code here
def Canny():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def Canny1():
        if len(Original_image_Size) > 2:
            a_Canny = int(numberChosen1.get())
            img = Original_Image[:, :, a_Canny - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)



            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=670)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')



            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Canny)+"Histogram")

                ax2.axvline(x=int(s_time1.val), color='r',label="Minimum")
                ax2.axvline(x=int(s_time2.val), color='g',label="Maximum")

                ax2.legend(loc='best')

                q = cv2.Canny(img, int(s_time1.val), int(s_time2.val))
                ax1.imshow(q, cmap='gray')





                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Segmented Image", fontsize=12, color="#333533")

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Canny)+"Histogram")

            ax2.legend(loc='best')

            def SaveI():
                f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                if f is None:
                    return

                filename = f.name

                cv2.imwrite(str(filename) + '.jpg', q)
                f.close()

            btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Segmented Image   ', padx=20, bd='5',
                             command=SaveI)
            btnw.place(x=400, y=0)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)



        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=670)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")

                ax2.axvline(x=int(s_time1.val), color='r', label="Minimum")
                ax2.axvline(x=int(s_time2.val), color='g', label="Maximum")

                ax2.legend(loc='best')

                q = cv2.Canny(img, int(s_time1.val), int(s_time2.val))
                ax1.imshow(q, cmap='gray')
                global q1
                q1=q

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Segmented Image", fontsize=12, color="#333533")

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")

            ax2.legend(loc='best')

            def SaveI():
                f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                if f is None:
                    return

                filename = f.name

                cv2.imwrite(str(filename) + '.jpg', q1)
                f.close()

            btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Segmented Image   ', padx=20, bd='5',
                             command=SaveI)
            btnw.place(x=400, y=0)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Canny1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Canny1)
        btn1.pack(anchor='w')

    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def AT():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def AT1():
        if len(Original_image_Size) > 2:
            a_AT = int(numberChosen1.get())
            img = Original_Image[:, :, a_AT - 1]

            def BT():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1,color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0,color='g')

                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(a_AT) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r',label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                              int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20, bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(a_AT) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            def BTI():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1, color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')


                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(a_AT) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r', label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)


                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(a_AT) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            btn5 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Mean Treshold Adaptive   ', padx=20,
                             bd='5', command=BT)
            btn5.place(x=0, y=100)
            btn6 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Gaussian Treshold Adaptive   ', padx=20,
                             bd='5', command=BTI)
            btn6.place(x=0, y=130)


        else:
            img = Original_Image

            def BT():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1, color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(1) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r', label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                              int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(1) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            def BTI():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1, color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(1) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r', label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(1) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            btn5 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Mean Treshold Adaptive   ', padx=20,
                             bd='5', command=BT)
            btn5.place(x=0, y=100)
            btn6 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Gaussian Treshold Adaptive   ', padx=20,
                             bd='5', command=BTI)
            btn6.place(x=0, y=130)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=AT1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=AT1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')


    root8.mainloop()


def OT():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    def OT1():
        if len(Original_image_Size) > 2:
            a_OT = int(numberChosen1.get())
            img = Original_Image[:, :, a_OT - 1]

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0,color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0,color='g')

            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_OT)+"Histogram")
                ax2.axvline(x=int(s_time2.val), color='g',label="Maximum")
                ax2.axvline(x=int(s_time1.val), color='r', label="Minimum")

                blur = cv2.GaussianBlur(img, (int(E1.get()), int(E1.get())), 0)
                ret3, q = cv2.threshold(blur, int(s_time1.val), int(s_time2.val),
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Treshhold Image", fontsize=12, color="#333533")

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax1.imshow(q, cmap='gray')

                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Invert Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_OT)+"Histogram")
            ax2.legend(loc='best')


            L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=200, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=330, y=720)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)




        else:
            img = Original_Image

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533")
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533")

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")
                ax2.axvline(x=int(s_time2.val), color='g', label="Maximum")
                ax2.axvline(x=int(s_time1.val), color='r', label="Minimum")

                blur = cv2.GaussianBlur(img, (int(E1.get()), int(E1.get())), 0)
                ret3, q = cv2.threshold(blur, int(s_time1.val), int(s_time2.val),
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Treshhold Image", fontsize=12, color="#333533")

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax1.imshow(q, cmap='gray')

                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Invert Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')

            L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=200, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=330, y=720)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=OT1)
        btn.place(x=0, y=60)

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=OT1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()

# Định nghĩa hàm mở trình chỉnh sửa hình ảnh
def open_image_editor():
    subprocess.run(["python", "Image_Editing.py"])

# Tạo cửa sổ chính của ứng dụng với kích thước 1920x1080
root1 = tk.Tk()
root1.geometry("1920x1080")
# Đặt ảnh biểu tượng cho cửa sổ
img = ImageTk.PhotoImage(file='logo.png')
root1.tk.call('wm', 'iconphoto', root1._w, img)

# Định nghĩa hàm để thay đổi kích thước hình ảnh khi cửa sổ thay đổi kích thước
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo #avoid garbage collection

# Mở ảnh ban đầu và sao chép nó
image = Image.open('Title.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
# Gắn ảnh vào nhãn và thay đổi kích thước khi cửa sổ thay đổi
label = ttk.Label(root1, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=tk.BOTH, expand = 'YES')

# Đặt tiêu đề cho cửa sổ
root1.title("VNU-UET - Group 16 - Image Processing Programme")

# Tạo thanh menu cho cửa sổ
menubar1 = tk.Menu(root1)


# Menu File với các lệnh liên quan đến file
filemenu = tk.Menu(menubar1, tearoff=0,activeborderwidth=4,activeforeground='red2',fg='blue',bg='thistle4',font=('Franklin Gothic Demi Cond', 11))
filemenu.add_command(label="New", command=OPEN)
filemenu.add_command(label="Open", command=OPEN)
filemenu.add_command(label="Save", command=OPEN)
filemenu.add_command(label="Save as...", command=OPEN)
filemenu.add_command(label="Close", command=OPEN)

# Thêm dấu phân cách và lệnh thoát
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root1.quit)
menubar1.add_cascade(label="File", menu=filemenu)

# Menu chỉnh sửa hình ảnh
image_editing_menu = tk.Menu(menubar1, tearoff=0)
image_editing_menu.add_command(label="Open Image Editor", command=open_image_editor)
menubar1.add_cascade(label="Image Editing", menu=image_editing_menu)

# Menu Segmentation với các lệnh liên quan đến phân đoạn ảnh
segmenu = tk.Menu(menubar1, tearoff=0, activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))

# Menu Edge Detection với các phương pháp phát hiện cạnh
Edge = tk.Menu(menubar1, tearoff=0, activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))
segmenu.add_cascade(label="Edge Detection", menu=Edge)
Edge.add_command(label="Robertz", command=Robertz)
Edge.add_command(label="Prewitt", command=Prewitt)
Edge.add_command(label="Sobel", command=Sobel)
Edge.add_command(label="Canny", command=Canny)

# Menu Tresholding với các phương pháp ngưỡng hóa
trmenu = tk.Menu(menubar1, tearoff=0, activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))
segmenu.add_cascade(label="Tresholding", menu=trmenu)
trmenu.add_command(label="Simple Tresholding", command=Tresholding)
trmenu.add_command(label="Adaptive Tresholding", command=AT)
trmenu.add_command(label="Otsu's Thresholding", command=OT)


menubar1.add_cascade(label="Segmentation", menu=segmenu)

# Thiết lập thanh menu cho cửa sổ
root1.config(menu=menubar1)

# Bắt đầu vòng lặp giao diện
root1.mainloop()

