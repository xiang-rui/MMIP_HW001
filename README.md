# MMIP_HW001
414830003 智慧科學暨綠能學院博士生 黃祥睿 (MMIP_HW001)

## Project Name
Image Processing Tool - `main_923.py`

## Overview

**Note:** This program is primarily designed to run via **GUI**.  
The **main image processing logic does not use any Python built-in libraries or external packages**, except for **Tkinter** and **PIL** which are used only for the GUI interface and saving images. All processing (reading RAW/BMP images, enhancement, resizing) is implemented manually.

`main_923.py` provides the following features:

Overview
This program is designed to perform fundamental image processing operations on a set of test images, including RAW and JPG formats. The tool allows users to read images, apply enhancement methods, perform resizing operations, extract key pixel data, and visualize the results through a graphical interface. All core image processing functions are custom-implemented without relying on external libraries except for GUI display and image visualization.

Features
- Read RAW images (512×512 grayscale) and common image formats such as BMP, JPG, and JPEG.
- Extract the centered 10×10 pixel values from each image.
- Apply image enhancement techniques including log-transform, gamma-transform, and negative image.
- Resize images using nearest-neighbor and bilinear interpolation methods across multiple scales: 32×32, 128×128, 256×512, 512×512, and 1024×512.
- Compare the effects of different resizing and enhancement methods visually.
- Display multiple images simultaneously in a GUI interface, including merged thumbnails and individual previews.
- Save all results into organized folders with clear filenames.

Implementation Details
- Custom Functions: All main processing functions, including reading, saving, enhancement, pixel extraction, and resizing, are implemented from scratch without using convenience libraries like OpenCV or NumPy.
- RAW Image Handling: RAW images are read as binary data and reshaped into 512×512 grayscale matrices.
- GUI: Tkinter is used for the graphical interface and PIL (Pillow) for image display. The GUI allows folder selection, process execution, and real-time visualization of results.
- Output Organization: Processed images are saved in structured folders, including Original, Enhancement (Log, Gamma, Negative), and Resize (NN, Bilinear). Centered 10×10 pixel values are saved to a text file.

How to Use
1. Launch the program:
   python main_923.py
2. Select the folder containing your images (minimum three RAW and three JPG/BMP images).
3. Click "Run" to process images.
4. Processed images will be saved in the `results` folder, organized by type. The GUI will display merged thumbnails and previews.

Output
- Original Images: Stored as PNG in `Original` folder.
- Enhancement Results: Stored as PNG in `Enhancement/Log`, `Enhancement/Gamma`, and `Enhancement/Negative` folders.
- Resized Images: Stored in `Resize/NN` and `Resize/Bilinear` folders with filenames indicating the interpolation method and target size, e.g., `goldhill_NN_32x32.png`.
- Merged Thumbnails: A 2×3 combined image of the original images.
- Centered Pixels: Extracted 10×10 pixel values saved in `center_pixels.txt`.

Notes
- The program strictly implements image processing functions manually, ensuring full understanding of underlying algorithms.
- The GUI and image display functionalities are the only parts utilizing external libraries.

1. Place dataset in `/media/user/driver/MMIP/data/data/`  
2. Run GUI:
python main_923.py
3. Browse and select dataset folder  
4. Click "Run Processing"  
5. Check `results_no_matplotlib/` folder for all outputs  
