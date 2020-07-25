# Webcam Paint

This application uses the OpenCV library to track objects of chosen colors and draw colored lines.

### Table of Contents

- [Description](#description)
- [References](#references)
- [Limitations](#limitations)
- [License](#license)

## Description

*Webcam Paint* allows users to specify HSV color ranges they want the program to detect, as well as colors to be associated with each HSV color range. 
Objects in the video capture that fall in these HSV color ranges become candidates for contour analysis. 
Depending contour analysis results, physical objects become eligible as pens for *Webcam Paint*. 
This program requires a functional webcam.

### Installation Dependencies

- Python 3.4 (or greater)
- [OpenCV](https://docs.opencv.org/master/d5/de5/tutorial_py_setup_in_windows.html)
- [NumPy](https://numpy.org/install/)

This program also uses the ``datetime``, ``os``, and ``tkinter`` libraries, which are members of the Python Standard Library.
Upon the successful installation of any libraries, restart any open IDLE windows before running ``remote.py``.

### How to Use
#### Setup
1. Download all repository files.
2. Ensure all [installation dependencies](#installation-dependencies) are met.
3. Run `remote.py`.

#### Color Input
1. In the ``Webcam Paint Remote`` window, click ``ADD COLORS``.
2. In the ``Color Selection`` window, adjust the values of the 6 sliders such that only the color you wish to track appears white in the ``Main mask`` window.
3. In the ``Color Selection`` window, click ``PICK COLOR`` to select the pen color to accompany the HSV color range you have determined in Step 2.
4. In the ``Color Selection`` window, click ``SAVE``.
5. Repeat steps 1-4 for each color range you wish to detect and its respective pen color.
6. In the ``Color Selection`` window, click ``DONE``.

#### Drawing
1. In the ``Webcam Paint Remote`` window, click ``DRAW``.
2. Hold colored objects to the camera and move them around to draw. Points will be drawn at the top-middle of the object, with certain [limitations](#limitations).

- ``TOGGLE DRAW`` toggles whether or not pens will actively draw on the canvas.
- ``CLEAR`` removes all drawn points from the canvas.
- ``PEN SIZE`` determine the size of circles drawn on the canvas from 0 to 30 pixels in radius.
- ``SAVE DRAWING`` saves the drawing on a black background as both a ``.png`` and a ``.jpg`` to the current directory.
- ``EXIT`` returns control of the program back to the ``Webcam Paint Remote`` window.

## Limitations
While the program supports the simultaneous detection of multiple different colored-pens, it does not support the simultaneous detection of multiple, same-colored pens. In other words, there can only be one active pen per color. If two objects of the same color are both present in the video capture, the object that occupies the largest area on the video capture will be designated as the pen.

## References
This program uses [OpenCV](https://github.com/opencv/opencv), an open-source computer vision library.

## License

MIT License

Copyright (c) 2020 Kai Wei Mo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
