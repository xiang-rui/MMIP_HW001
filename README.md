# MMIP_HW001
414830003 智慧科學暨綠能學院博士生 黃祥睿 (MMIP_HW001)

## Project Name
Image Processing Tool - `main_923.py`

## Overview

**Note:** This program is primarily designed to run via **GUI**.  
The **main image processing logic does not use any Python built-in libraries or external packages**, except for **Tkinter** and **PIL** which are used only for the GUI interface and saving images. All processing (reading RAW/BMP images, enhancement, resizing) is implemented manually.

`main_923.py` provides the following features:

1. **Image Reading**  
   - Supports RAW grayscale images (512x512)  
   - Supports BMP / JPG / JPEG color images, automatically converted to grayscale  

2. **Image Enhancement**  
   - Log-transform  
   - Gamma-transform  
   - Image negative  

3. **Image Downsampling / Upsampling**  
   - Nearest-Neighbor (NN) interpolation  
   - Bilinear interpolation  
   - Supports any size conversion (e.g., 512x512 → 128x128, 32x32 → 512x512, etc.)  

4. **Center Pixel Extraction**  
   - Extracts the **center 10x10 pixels** from each image  
   - Saves values to `center_pixels.txt`  

5. **Automatic Result Saving**  
   - All results are saved in `results_no_matplotlib` folder:  
     results_no_matplotlib/
         Original/           # Original images
         Enhancement/
             Log/           # Log-transform
             Gamma/         # Gamma-transform
             Negative/      # Image negative
         Resize/
             NN/            # Nearest-Neighbor results
             Bilinear/      # Bilinear results
         center_pixels.txt   # Center 10x10 pixel values

6. **GUI Operation**  
   - Select the dataset folder  
   - Click "Run Processing" to execute all operations  
   - Status is displayed in the GUI  

---

## Environment Requirements

- Python 3.8.8  
- Packages:  
pip install pillow
- Tkinter is included in standard Python distribution  

---

## Usage

### 1. Prepare Your Dataset
Place images in a folder, for example:  
/media/user/driver/MMIP/data/data/
    baboon.bmp
    boat.bmp
    F16.bmp
    goldhill.raw
    lena.raw
    peppers.raw

### 2. Run the Program

#### Option 1: GUI Mode
python main_923.py
- A GUI window will appear  
- Click "Browse" to select the dataset folder  
- Click "Run Processing" to start  
- Status and completion message will be displayed  

#### Option 2: Directly Specify Data Path
You can specify the dataset path directly in the script by modifying the bottom section:

if __name__ == "__main__":
    data_path = "/media/user/driver/MMIP/data/data/"  # <-- change to your folder path
    process_images(data_path)

Then run:  
python main_923.py
- The program will automatically process all images and save results  

---

## Output Results

1. **Original Images**  
   - Saved in `results_no_matplotlib/Original/`  

2. **Enhanced Images**  
   - Log-transform → `results_no_matplotlib/Enhancement/Log/`  
   - Gamma-transform → `results_no_matplotlib/Enhancement/Gamma/`  
   - Image negative → `results_no_matplotlib/Enhancement/Negative/`  

3. **Resized Images**  
   - Nearest-Neighbor → `results_no_matplotlib/Resize/NN/`  
   - Bilinear → `results_no_matplotlib/Resize/Bilinear/`  

4. **Center 10x10 Pixels**  
   - Saved in `results_no_matplotlib/center_pixels.txt`  

---

## Notes

1. RAW images must be **512x512 grayscale**  
2. BMP / JPG / JPEG images will automatically be converted to grayscale  
3. If the selected folder contains no images, the program will display a warning  
4. The program **does not display images**, all results are automatically saved  

---

## Example Execution Flow

1. Place dataset in `/media/user/driver/MMIP/data/data/`  
2. Run GUI:
python main_923.py
3. Browse and select dataset folder  
4. Click "Run Processing"  
5. Check `results_no_matplotlib/` folder for all outputs  
