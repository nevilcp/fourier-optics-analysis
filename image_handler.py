"""Load an image as grayscale, view its spectrum and apply frequency-domain filters."""

from math import pi

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import fftpack


class ImageHandler:
    """A grayscale image together with its centred 2-D Fourier transform.

    `fName` is an optional image path, loaded in grayscale mode ("L").
    `extend` is ignored; it exists only for compatibility.
    """

    def __init__(self, fName=None, extend=False):
        if fName is not None:
            self.orig = Image.open(fName).convert("L")
            self.image = Image.open(fName).convert("L")
            self.extend = False
            self.four = self.fourier()

    def loadImage(self, image, extend=False):
        """Set the current image (PIL image or array) and recompute its spectrum.

        `extend` is ignored.
        """
        self.image = image
        self.four = self.fourier()

    def fourier(self):
        """Return the 2-D FFT of the current image, with zero frequency at the centre."""
        return fftpack.fftshift(fftpack.fft2(self.image))

    def showFourier(self):
        """Plot the log power spectrum, with both frequency axes spanning -pi to pi.

        Requires a LaTeX installation for the axis labels.
        """
        psd2D = np.log(np.abs(self.four) ** 2 + 1)
        (height, width) = psd2D.shape
        plt.figure(figsize=(10, 10 * height / width), facecolor="white")
        plt.clf()
        plt.rc("text", usetex=True)
        plt.xlabel(r"$\omega_1$", fontsize=24)
        plt.ylabel(r"$\omega_2$", fontsize=24)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.imshow(psd2D, cmap="Greys_r", extent=[-pi, pi, -pi, pi], aspect="auto")
        plt.show()

    def showImage(self):
        """Open the current image in the system viewer."""
        self.image.show()

    def inverseFourier(self):
        """Set `self.image` to the inverse FFT of `self.four`, rounded to integers."""
        self.image = Image.fromarray(np.round(np.real(fftpack.ifft2(fftpack.ifftshift(self.four)))))

    def applyFilter(self, fil):
        """Apply the `Filter` `fil` to the spectrum and rebuild the image from it."""
        self.four = fil.modify(self.four)
        self.inverseFourier()

    def getImage(self):
        """Return the current image."""
        return self.image

    def getOriginal(self):
        """Return the grayscale image as first loaded."""
        return self.orig

    def convolve(self, kernel):
        """Convolve the current image with `kernel` in the spatial domain."""
        self.convolveH(np.array(self.image), kernel)

    def convolveH(self, matrix, kernel):
        """Slide `kernel` over `matrix` (unflipped, so strictly a correlation).

        Pixels beyond the border count as zero. The result becomes the current
        image and the spectrum is recomputed.
        """
        newmatrix = []
        for y in range(len(matrix)):
            newrow = []
            newmatrix.append(newrow)
            for x in range(len(matrix[0])):
                newvalue = 0
                for ky in range(len(kernel)):
                    for kx in range(len(kernel[0])):
                        yind = int(y + (ky - len(kernel) // 2))
                        xind = int(x + (kx - len(kernel[0]) // 2))
                        if 0 <= yind < len(matrix) and 0 <= xind < len(matrix[0]):
                            newvalue += matrix[yind][xind] * kernel[ky][kx]
                newrow.append(newvalue)
        self.image = Image.fromarray(np.array(newmatrix))
        self.four = self.fourier()
