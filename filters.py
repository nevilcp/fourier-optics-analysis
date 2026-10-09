"""Frequency-domain filter masks for centred (fftshift-ed) 2-D spectra."""

from abc import ABC, abstractmethod

import numpy as np


class Filter(ABC):
    """Base class for filters that mask a 2-D array element-wise.

    `c` is an optional colour tag stored as `self.color`; no filter uses it.
    """

    def __init__(self, c=0):
        self.color = c
        self.points = set()

    def getPoints(self):
        """Return `self.points`, a set that no subclass populates."""
        return self.points

    @abstractmethod
    def modify(self, image):
        """Return `image` multiplied by this filter's mask."""


class CircleFilter(Filter):
    """Circular or ring-shaped mask centred on the spectrum. Radii are in pixels.

    With only `radiusI`, the mask is a high-pass filter (`outside=True`) or a
    low-pass filter (`outside=False`). With `radiusO` as well, it is a band-stop
    filter (`outside=True`, ring removed) or a band-pass filter (`outside=False`,
    ring kept). `radiusO=-1` means no outer radius.
    """

    def __init__(self, radiusI, radiusO=-1, outside=True, c=0):
        super().__init__(c)
        self.innerRadius = radiusI
        self.outerRadius = radiusO
        self.outside = outside

    def showMultImage(self, image):
        """Return the 0/1 mask for an array shaped like `image`."""
        (height, width) = image.shape
        # Start from the background, then paint the larger circle before the smaller one.
        if self.outside:
            mult = [[1] * width for _ in range(height)]
            if self.outerRadius != -1:
                self.fillCircle(mult, 0, self.outerRadius, width, height)
                self.fillCircle(mult, 1, self.innerRadius, width, height)
            else:
                self.fillCircle(mult, 0, self.innerRadius, width, height)
        else:
            mult = [[0] * width for _ in range(height)]
            if self.outerRadius != -1:
                self.fillCircle(mult, 1, self.outerRadius, width, height)
                self.fillCircle(mult, 0, self.innerRadius, width, height)
            else:
                self.fillCircle(mult, 1, self.innerRadius, width, height)
        return np.array(mult)

    def modify(self, image):
        """Return `image` multiplied by the circular mask."""
        return np.multiply(image, self.showMultImage(image))

    def fillCircle(self, arr, num, radius, width, height):
        """Set cells of `arr` strictly within `radius` of the centre to `num`, in place."""
        center = (width / 2, height / 2)
        for i in range(height):
            for j in range(width):
                if (float(i) - center[1]) ** 2 + (float(j) - center[0]) ** 2 < float(radius) ** 2:
                    arr[i][j] = num


class LineFilter(Filter):
    """Mask of ones on a `width` x `height` grid, with lines zeroed via `addLine`."""

    def __init__(self, width, height, c=0):
        super().__init__(c)
        self.width = width
        self.height = height
        self.mult = [[1] * width for _ in range(height)]

    def addLine(self, x1, y1, x2, y2, pixelWidth=1):
        """Zero the line from (x1, y1) to (x2, y2), `pixelWidth` cells thick.

        Coordinates are integer (x, y) pixels. Points off the grid are skipped.
        Shallow lines are thickened downwards, steep lines to the right.
        """
        # Iterate along x for shallow lines (|dx| > |dy|), along y for steep ones.
        wdown = abs((x1 - x2) + 1) / abs((y1 - y2) + 1) > 1

        if wdown:
            # Order the endpoints so x increases left to right.
            p1, p2 = ((x1, y1), (x2, y2)) if x1 < x2 else ((x2, y2), (x1, y1))

            for x in range(p1[0], p2[0] + 1):
                y = (p2[1] - p1[1]) * (x - p1[0]) / (p2[0] - p1[0]) + p1[1]

                if 0 <= y < self.height and 0 <= x < self.width:
                    self.mult[int(y)][int(x)] = 0

                # Thicken the line downwards.
                ny2 = y
                pw = pixelWidth
                while pw > 1:
                    ny2 += 1
                    if 0 <= ny2 < self.height and 0 <= x < self.width:
                        self.mult[int(ny2)][int(x)] = 0
                    pw -= 1

        else:
            # Order the endpoints so y increases top to bottom.
            p1, p2 = ((x1, y1), (x2, y2)) if y1 < y2 else ((x2, y2), (x1, y1))

            for y in range(p1[1], p2[1] + 1):
                x = (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1]) + p1[0]

                if 0 <= y < self.height and 0 <= x < self.width:
                    self.mult[int(y)][int(x)] = 0

                # Thicken the line to the right.
                nx2 = x
                pw = pixelWidth
                while pw > 1:
                    nx2 += 1
                    if 0 <= y < self.height and 0 <= nx2 < self.width:
                        self.mult[int(y)][int(nx2)] = 0
                    pw -= 1

    def modify(self, image):
        """Return `image` multiplied by the line mask."""
        return np.multiply(image, self.mult)
