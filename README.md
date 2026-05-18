# Fourier Optics: Frequency Domain Image Processing and Analysis

## 1. Abstract / Overview

The primary objective of this project is to investigate and implement two-dimensional frequency domain filtering techniques for digital image processing. By leveraging the convolution theorem and Fourier transform properties, the project demonstrates the manipulation of spatial frequencies to achieve phenomena such as low-pass (blurring/smoothing), high-pass (edge detection), and custom spectral filtering. This work provides a rigorous programmatic foundation for understanding optical principles simulated in a digital computing environment.

## 2. Methodology

The core computational approach relies on the Discrete Fourier Transform (DFT), specifically optimized via the Fast Fourier Transform (FFT) algorithm computationally backed by SciPy. 

*   **Coordinate Transformation and Shift:** Images are transformed from the spatial domain $(x, y)$ to the spatial frequency domain $(u, v)$. The zero-frequency (DC) component is systematically shifted to the center of the spectrum for symmetric filter application.
*   **Filter Implementation (`Filter.py`):** Mathematical filter masks $H(u,v)$, specifically a `CircleFilter` (acting as ideal low-pass, high-pass, or band-pass filters based on inner/outer radii) and a `LineFilter`, are dynamically generated. These matrices are multiplied point-wise with the shifted Fourier spectrum $F(u,v)$ of the input image. 
*   **Image Handling Iteration (`ImageHandler.py`):** Encapsulates the pipeline of gray-scale conversion (via Pillow), spatial domain convolution, spectrum visualization (mapping axes from $-\pi$ to $\pi$ on a logarithmic scale), and executing the Inverse Fast Fourier Transform (IFFT) to reconstruct the filtered spatial domain image $g(x,y)$.

$$ g(x,y) = \mathcal{F}^{-1} \{ F(u,v) \cdot H(u,v) \} $$

## 3. Dataset & Preprocessing

The spatial inputs utilized in this study consist of various standardized grayscale and RGB images (stored in the `/pics` directory, including diverse patterns like sine waves and photographic imagery). 

**Preprocessing Pipeline:**
1. **Channel Reduction:** Multi-channel images are converted to single-channel (`L` mode) matrices representing grayscale intensities via the Pillow library.
2. **Padding and Extraction:** Array padding functions structurally support kernel convolution operations directly into numerical matrices representing real magnitudes.

## 4. Results & Discussion

The implementation successfully demonstrates the theoretical expectations of spatial frequency manipulation across $14$ parameterized tests found in the main notebook. 

*   **Low-Pass / High-Pass Filtering:** Demonstrated directly via circle filters; effectively attenuates high-frequency features or isolates sharp transitions.
*   **Pattern Extraction:** Tests on pure sine-wave images visually correlate spatial orientation with distinct impulses located within the respective spectral origin axes.

