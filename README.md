# Fourier Optics: Frequency Domain Image Processing and Analysis

## 1. Abstract / Overview

This project implements two-dimensional frequency-domain filtering for digital images. Using the convolution theorem and the properties of the Fourier transform, it shows how manipulating spatial frequencies produces low-pass (smoothing), high-pass (sharp transitions) and custom spectral filtering. It serves as a hands-on, programmatic introduction to the principles of Fourier optics.

## 2. Methodology

The approach relies on the Discrete Fourier Transform (DFT), computed with the Fast Fourier Transform (FFT) from SciPy.

*   **Coordinate Transformation and Shift:** Images are transformed from the spatial domain $(x, y)$ to the spatial-frequency domain $(u, v)$. The zero-frequency (DC) component is shifted to the centre of the spectrum so that filter masks can be centred on it.
*   **Filter Implementation (`filters.py`):** Filter masks $H(u,v)$ are generated on demand: `CircleFilter` (ideal low-pass, high-pass, band-pass or band-stop, depending on its radii and `outside` flag) and `LineFilter` (zeroed lines). Each mask is multiplied point-wise with the shifted spectrum $F(u,v)$ of the image.
*   **Image Handling Iteration (`image_handler.py`):** `ImageHandler` wraps the pipeline: grayscale conversion (Pillow), spatial-domain convolution, log-scale spectrum plots with axes from $-\pi$ to $\pi$, and the inverse FFT that reconstructs the filtered image $g(x,y)$.

$$ g(x,y) = \mathcal{F}^{-1} \{ F(u,v) \cdot H(u,v) \} $$

## 3. Dataset & Preprocessing

The inputs are grayscale and colour images in `pics/`, including synthetic sine-wave and line patterns and photographs.

**Preprocessing:**
1. **Channel reduction:** Pillow converts every image to single-channel grayscale (`L` mode).
2. **Kernel padding:** The notebook's `padKernal` helper zero-pads a convolution kernel to the image size, keeping it centred.

## 4. Results & Discussion

The 14 numbered cases in `fourier_analysis.ipynb` (0–13) match the theoretical expectations.

*   **Low-Pass / High-Pass Filtering:** Circle filters remove high-frequency detail (low-pass) or keep only sharp transitions (high-pass); ring filters give band-pass and band-stop behaviour.
*   **Sine-wave spectra:** A pure sine-wave image produces distinct impulses in its spectrum, and the impulses' orientation follows the stripes' orientation.

## 5. Setup & Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open `fourier_analysis.ipynb` in Jupyter (install `jupyterlab` or `ipykernel` separately) and run all cells. Each of the 14 cases is run by `run_case()`.

`ImageHandler.showFourier()` renders its axis labels with LaTeX, so it needs a LaTeX installation.

Lint and format with [ruff](https://docs.astral.sh/ruff/):

```bash
ruff check .
ruff format .
```

## 6. Project Structure

| Path | Purpose |
|---|---|
| `filters.py` | `CircleFilter` and `LineFilter` spectrum masks |
| `image_handler.py` | `ImageHandler`: loading, FFT, filtering, convolution |
| `fourier_analysis.ipynb` | The 14 demonstration cases |
| `pics/` | Input images |
| `requirements.txt` | Runtime dependencies |
| `ruff.toml` | Lint and format configuration |
