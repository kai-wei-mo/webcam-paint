from tkinter import *
from tkinter import colorchooser

import cv2
import numpy as np


class SliderGUI:
    def __init__(self):
        """Create GUI with 6 Scale objects (for HSV color range) and a respective color chooser.
        Include SAVE and DONE buttons."""

        self.is_done = False
        self.color_hex = '#000000'

        self.labels = []
        self.labels.append(Label(master, text="min_hue"))
        self.labels.append(Label(master, text="max_hue"))
        self.labels.append(Label(master, text="min_sat"))
        self.labels.append(Label(master, text="max_sat"))
        self.labels.append(Label(master, text="min_val"))
        self.labels.append(Label(master, text="max_val"))

        self.scales = []
        self.scales.extend(Scale(master, from_=0, to=179, length=500, orient=HORIZONTAL) for _ in range(2))
        self.scales.extend(Scale(master, from_=0, to=255, length=500, orient=HORIZONTAL) for _ in range(4))

        self.color_sample = Label(master, bg=self.color_hex)
        self.color_button = Button(master, text="PICK COLOR", command=lambda: self.choose_color())
        self.save_button = Button(master, text="SAVE", command=lambda: self.save_color())
        self.done_button = Button(master, text="DONE", command=lambda: self.update_done())

        # default values of Scales
        self.scales[0].set(0)
        self.scales[1].set(179)
        self.scales[2].set(0)
        self.scales[3].set(255)
        self.scales[4].set(0)
        self.scales[5].set(255)

        # pack elements to master
        for j in range(6):
            self.labels[j].grid(row=j, column=0, padx=4, pady=4)
            self.scales[j].grid(row=j, column=1)

        self.color_sample.grid(row=1, column=2, pady=4, sticky=N + S + E + W)
        self.color_button.grid(row=3, column=2, pady=4, sticky=N + S + E + W)
        self.save_button.grid(row=4, column=2, pady=4, sticky=N + S + E + W)
        self.done_button.grid(row=5, column=2, pady=4, sticky=N + S + E + W)

    def choose_color(self):
        """Store the hexadecimal value of the user-chosen color.
        Updates color of color_sample on GUI."""
        color_code = colorchooser.askcolor(title="Choose Color")
        self.color_hex = color_code[1]
        self.color_sample.config(bg=self.color_hex)

    def get_scale_values(self):
        """Returns the values of the 6 Scales as one list."""
        # [min_hue, max_hue, min_sat, max_sat, min_val, max_val]
        return [x.get() for x in self.scales]

    def save_color(self):
        """Save the hexadecimal color value and the 6 Scale values into a .txt file."""
        scale_values = self.get_scale_values()
        data = [self.color_hex, scale_values]
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

win = SliderGUI()
camera = cv2.VideoCapture(0)  # default camera, uses machine's backend

if not camera.isOpened():
    print("Camera not detected.")
    sys.exit()

while True:
    if win.is_done:
        break

    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    master.update_idletasks()
    master.update()

    # [min_hue, max_hue, min_sat, max_sat, min_val, max_val]
    values = win.get_scale_values()

    for i in range(0, 2, 6):
        # if min_xxx greater than max_xxx, set min_xxx equal to max_xxx
        if values[i] > values[i + 1]:
            win.scales[i].set(win.scales[i + 1].get())

    # find HSV color ranges used for mask transformations
    lower_range = np.array([values[0], values[2], values[4]])
    upper_range = np.array([values[1], values[3], values[5]])

    # if video capture is successful
    if ret:
        # use frame to create HSV to create mask
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # display frame and mask
        cv2.imshow("Main mask", mask)
        cv2.imshow('Video Capture', frame)

# release capture
camera.release()
cv2.destroyAllWindows()
