import os
from os import path
from tkinter import *
from tkinter import messagebox


def run_file(filename):
    """Execute shell command."""
    os.system(filename)


def clear_colors(file_name):
    """Asks the user for confirmation when clearing saved colors.
    If provided, the .txt file is deleted and the user is notified of the successful deletion """
    if path.exists('colors.txt') and os.path.getsize('colors.txt') > 0:
        if messagebox.askyesno('Clear contents of colors.txt',
                               'Are you sure you want to delete all your saved colors?'):
            with open(file_name, 'w') as file:
                file.close()
            messagebox.showinfo('Success', 'All saved colors were successfully deleted.')
    else:
        messagebox.showinfo('Notification', 'You have no colors saved.')


master = Tk()
master.title("Webcam Paint Remote")

b_color_input = Button(master, text="ADD COLORS", command=lambda: run_file('color_input.py'))
b_paint = Button(master, text="DRAW", command=lambda: run_file('draw_mode.py'))
b_clear_colors = Button(master, text="DELETE SAVED COLORS", command=lambda: clear_colors('colors.txt'))

b_color_input.pack()
b_paint.pack()
b_clear_colors.pack()

if __name__ == '__main__':
    master.mainloop()
