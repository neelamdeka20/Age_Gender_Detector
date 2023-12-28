# Importing necessary libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *

from PIL import Image, ImageTk
import numpy as np

# Loading the model
from keras.models import load_model

model = load_model('model_weights.h5')

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age and Gender Detector')
top.configure(background='#CDCDCD')

# Initializing the labels(One for age and other for gender)
label1 = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
label2 = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)

# Defining detect function which detects the age and gender of person in image using the model
def detect(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((48, 48))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    image = np.delete(image, 0, 1)
    image = np.resize(image, (48, 48, 3))
    print(image.shape)
    gender_f = ['Male', 'Female']
    image = np.array([image])/255
    pred = model.predict(image)
    age = int(np.round(pred[1][0]))
    gender = int(np.round(pred[0][0]))
    print('Predicted Age is ', str(age))
    print('Predicted Gender is ', gender_f[gender])
    label1.configure(foreground='#011638', text=age)
    label2.configure(foreground='#011638', text=gender_f[gender])

# Defining show detect button
def show_detect_button(file_path):
    detect_b = Button(top, text='Detect Image', command=lambda: detect(file_path), padx=10, pady=5)
    detect_b.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
    detect_b.place(relx=0.79, rely=0.46)

# Defining upload image button
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_detect_button(file_path)
    except:
        pass

upload = Button(top, text='Upload an Image', command=upload_image, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)

label1.pack(side='bottom', expand=True)
label2.pack(side='bottom', expand=True)
heading = Label(top, text='Age and Gender Detector', pady=20, font=('arial', 20, 'bold'))
heading.configure(background='#CDCDCD', foreground='#364156')
heading.pack()
top.mainloop()