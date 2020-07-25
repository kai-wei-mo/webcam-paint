from tkinter import *
from tkinter import colorchooser

import cv2
import numpy as np


class SliderGUI:
    def __init__(self):
        """Create GUI with 6 Scale objects (for HSV color range) and a respective color chooser button.
        Include SAVE and DONE buttons."""

        self.is_done = False
        self.color_hex = '#000000'

        self.label1 = Label(master, text="min_hue")
        self.label2 = Label(master, text="max_hue")
        self.label3 = Label(master, text="min_sat")
        self.label4 = Label(master, text="max_sat")
        self.label5 = Label(master, text="min_val")
        self.label6 = Label(master, text="max_val")
        self.hue1 = Scale(master, from_=0, to=179, length=500, orient=HORIZONTAL)
        self.hue2 = Scale(master, from_=0, to=179, length=500, orient=HORIZONTAL)
        self.sat1 = Scale(master, from_=0, to=255, length=500, orient=HORIZONTAL)
        self.sat2 = Scale(master, from_=0, to=255, length=500, orient=HORIZONTAL)
        self.val1 = Scale(master, from_=0, to=255, length=500, orient=HORIZONTAL)
        self.val2 = Scale(master, from_=0, to=255, length=500, orient=HORIZONTAL)
        self.color_sample = Label(master, bg=self.color_hex)
        self.color_button = Button(master, text="PICK COLOR", command=lambda: self.choose_color())
        self.save_button = Button(master, text="SAVE", command=lambda: self.save_color())
        self.done_button = Button(master, text="DONE", command=lambda: self.update_done())

        # default values of Scales
        self.hue1.set(0)
        self.hue2.set(179)
        self.sat1.set(0)
        self.sat2.set(255)
        self.val1.set(0)
        self.val2.set(255)

        self.label1.grid(row=0, column=0, padx=4, pady=4)
        self.label2.grid(row=1, column=0, padx=4, pady=4)
        self.label3.grid(row=2, column=0, padx=4, pady=4)
        self.label4.grid(row=3, column=0, padx=4, pady=4)
        self.label5.grid(row=4, column=0, padx=4, pady=4)
        self.label6.grid(row=5, column=0, padx=4, pady=4)

        self.hue1.grid(row=0, column=1)
        self.hue2.grid(row=1, column=1)
        self.sat1.grid(row=2, column=1)
        self.sat2.grid(row=3, column=1)
        self.val1.grid(row=4, column=1)
        self.val2.grid(row=5, column=1)

        self.color_sample.grid(row=1, column=2, pady=4, sticky=W + E + N + S)
        self.color_button.grid(row=3, column=2, pady=4, sticky=W + E + N + S)
        self.save_button.grid(row=4, column=2, pady=4, sticky=W + E + N + S)
        self.done_button.grid(row=5, column=2, pady=4, sticky=W + E + N + S)

    def choose_color(self):
        """Store the hexadecimal value of the user-chosen color.
        Updates color of color_sample on GUI."""
        color_code = colorchooser.askcolor(title="Choose Color")
        self.color_hex = color_code[1]
        self.color_sample.config(bg=self.color_hex)

    def save_color(self):
        """Save the hexadecimal color value and the 6 Scale values into a .txt file."""
        list_of_values = [self.hue1.get(), self.hue2.get(),
                          self.sat1.get(), self.sat2.get(),
                          self.val1.get(), self.val2.get()]

        data = [self.color_hex, list_of_values]
        with open('colors.txt', 'a') as file:
            file.write(str(data) + '\n')
        file.close()
        print(data)

    def update_done(self):
        """Set is_done to True to be used to break out of the main loop."""
        self.is_done = True


def do_nothing():
    pass


master = Tk()
master.title('Color Selection')
master.geometry('675x275')
master.protocol("WM_DELETE_WINDOW", do_nothing)  # user cannot use [X] to exit

sliders = SliderGUI()
camera = cv2.VideoCapture(0)  # default camera, uses machine's backend

if not camera.isOpened():
    print("Camera not detected.")
    sys.exit()

while True:
    if sliders.is_done:
        break

    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    master.update_idletasks()
    master.update()

    # update the 6 values that determine HSV color range
    min_hue = sliders.hue1.get()
    max_hue = sliders.hue2.get()
    min_sat = sliders.sat1.get()
    max_sat = sliders.sat2.get()
    min_val = sliders.val1.get()
    max_val = sliders.val2.get()

    # if min greater than max, set min equal to max
    if min_hue > max_hue:
        sliders.hue1.set(sliders.hue2.get())
    if min_sat > max_sat:
        sliders.sat1.set(sliders.sat2.get())
    if min_val > max_val:
        sliders.val1.set(sliders.val2.get())

    # find range of HSV color, to be used for mask transformations
    lower_range = np.array([min_hue, min_sat, min_val])
    upper_range = np.array([max_hue, max_sat, max_val])

    # if frame capture is successful, use frame to find HSV to create mask
    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # display frame and mask
        cv2.imshow("Main mask", mask)
        cv2.imshow('Video Capture', frame)

# release capture
camera.release()
cv2.destroyAllWindows()
