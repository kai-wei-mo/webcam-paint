from datetime import datetime
from tkinter import *
from tkinter import messagebox

import cv2
import numpy as np


class SettingsGUI:
    def __init__(self):
        """Create GUI with toggle and clear buttons, pen size scale, and save and exit buttons."""
        self.toggle = Button(master, text="TOGGLE DRAW", relief="raised", command=lambda: self.toggle_draw())
        self.clear = Button(master, text="CLEAR", command=lambda: self.clear_points())
        self.scale_label = Label(master, text="PEN SIZE:")
        self.pen_size = Scale(master, from_=0, to=30, length=90, orient=HORIZONTAL, showvalue=0,
                              command=lambda x=None: self.update_scale_label())
        self.var = StringVar()
        self.scale_value = Label(master, textvariable=self.var)
        self.save = Button(master, text="SAVE DRAWING", command=lambda: save_drawing())
        self.exit = Button(master, text="EXIT", command=lambda: self.update_is_done())

        # default values
        self.pen_size.set(15)
        self.var.set(str(15))
        self.is_drawing = True
        self.is_clear = False
        self.is_done = False

        self.toggle.pack()
        self.clear.pack()
        self.scale_label.pack()
        self.pen_size.pack()
        self.scale_value.pack()
        self.save.pack()
        self.exit.pack()

    def toggle_draw(self):
        """Toggle button will appear sunken or raised depending on its boolean value."""
        if self.toggle.config('relief')[-1] == 'sunken':
            self.toggle.config(relief="raised")
        else:
            self.toggle.config(relief="sunken")
        self.is_drawing = not self.is_drawing

    def update_scale_label(self):
        """Update the label underneath the pen_size Scale."""
        self.var.set(str(self.pen_size.get()))

    def clear_points(self):
        """Set is_clear to True to clear all existing points."""
        self.is_clear = True

    def update_is_done(self):
        """Set is_done to True to be used to break out of the main loop."""
        self.is_done = True


def do_nothing():
    pass


def hex_to_rgb(hex_col):
    """Takes a hexadecimal color in the form '#xxxxxx' and returns its RGB value as a tuple."""
    hex_col = hex_col.lstrip('#')
    return tuple(int(hex_col[n:n + 2], 16) for n in (0, 2, 4))


def get_ranges(col):
    """Organizes a list of the 6 Slider values for the creation of HSV masks."""
    # col = [min_hue, max_hue, min_sat, max_sat, min_val, max_val]
    lower_range = np.array([col[0], col[2], col[4]])  # min_hue, min_sat, min_val
    upper_range = np.array([col[1], col[3], col[5]])  # max_hue, max_sat, max_val

    return lower_range, upper_range


def get_contour_points(img):
    """Takes HSV mask and returns x and y coordinates for the top-middle of a contoured object.
    This function recognizes rectangles with a mild degree of flexibility from GaussianBlur."""
    x, y, w, h = 0, 0, 0, 0
    # img = cv2.GaussianBlur(img, (5, 5), 1)
    # retrieves only the extreme outer contours
    _, thresh = cv2.threshold(img, 40, 255, 0)

    # if cv2.__version__[0] >= 3:
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        # draw identified contours in blue
        cv2.drawContours(canvas, contours, -1, 255, 2)

        # find the biggest contour (c) by the area
        c = max(contours, key=cv2.contourArea)

        # if the largest contour occupies >= 500px
        if cv2.contourArea(c) >= 500:
            # draw the biggest contour's bounding rect in green
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 255, 0), 3)

    if x == 0 and y == 0:
        return None

    # draw green circle around pen tip
    cv2.circle(canvas, (x + w // 2, y), 50, (0, 255, 0), 3)
    return x + w // 2, y


def draw_circles(pts, surface):
    """Draws all registered points on the specified surface."""
    for pt in pts:
        rgb = hex_to_rgb(pt[1])
        cv2.circle(surface, (pt[0][0], pt[0][1]), pt[2], (rgb[2], rgb[1], rgb[0]), cv2.FILLED)


def save_drawing():
    """Draw all points onto a black image and save image to current directory.
    The name of the image reflects the current timestamp."""
    image = np.ones_like(frame)
    draw_circles(points, image)

    date_time_obj = str(datetime.now()).replace(':', '')
    cv2.imwrite(f'{date_time_obj}.jpg', image)
    cv2.imwrite(f'{date_time_obj}.png', image)
    messagebox.showinfo('Image saved', 'The image has been saved to the current directory.')


hex_codes = []  # hex_codes = ['#000000', ...]
colors = []  # colors = [[0, 179, 0, 255, 0, 255], ...]
ranges = []  # ranges = [([0, 0, 0,], [179, 255, 255]), ...]
points = []  # points = [[(x, y), '#000000', 15], ...]

# load color information from colors.txt into colors[] and hex_codes[]
try:
    with open('colors.txt', 'r') as file:
        for line in file:
            temp = eval(line)
            hex_codes.append(temp[0])
            colors.append(temp[1])
except FileNotFoundError:
    messagebox.showinfo('Error', 'The file "colors.txt" does not exist. Please click "ADD COLORS" to add colors.')
    sys.exit()

num_of_colors = len(colors)

for color in colors:  # [[0, 179, 0, 255, 0, 255], ...]
    ranges.append(get_ranges(color))

camera = cv2.VideoCapture(0)  # default camera, use machine's backend

if not camera.isOpened():
    print("Camera not detected.")
    sys.exit()

camera.set(10, 175)
# frame length width?

master = Tk()

master.title('SETTINGS')
master.geometry('175x175')
master.protocol("WM_DELETE_WINDOW", do_nothing)  # user cannot use [X] to exit
settings = SettingsGUI()

while True:
    if settings.is_done:
        break

    # read VideoCapture input and flip horizontally
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # clear all existing points
    if settings.is_clear:
        points = []
        settings.is_clear = False

    canvas = frame[:]  # numpy matrix identical to VideoCapture input
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if not num_of_colors:
        messagebox.showinfo('No colors found',
                            'There are no colors in the registry. Please click "ADD COLORS" to add colors.')
        break
    for i in range(num_of_colors):
        # get HSV color range based on the 6 Scale values
        mask = cv2.inRange(hsv, ranges[i][0], ranges[i][1])
        small = cv2.resize(mask, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow(str(colors[i]), small)

        # if is_drawing is toggled on, find contour points and append to points
        if settings.is_drawing:
            contour_points = get_contour_points(mask)
            if contour_points:  # if contour_points = get_contour_points(mask) (?)
                points.append([contour_points, hex_codes[i], settings.pen_size.get()])

        # draw all existing points onto canvas
        draw_circles(points, canvas)

    cv2.imshow("Canvas", canvas)

    # equivalent to master.mainloop() but doesn't open second thread
    master.update_idletasks()
    master.update()

# release capture
camera.release()
cv2.destroyAllWindows()
