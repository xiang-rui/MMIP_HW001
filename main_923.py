import os
import math
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# -------------------------------
# 功能函數
# -------------------------------
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def read_raw_gray(filename, width=512, height=512):
    with open(filename, "rb") as f:
        data = f.read()
    img = [[data[row * width + col] for col in range(width)] for row in range(height)]
    return img


def read_bmp(filename):
    img = Image.open(filename).convert("L")
    img_data = list(img.getdata())
    w, h = img.size
    img_2d = [img_data[i * w:(i + 1) * w] for i in range(h)]
    return img_2d


def save_image(img, path):
    h = len(img)
    w = len(img[0])
    im = Image.new("L", (w, h))
    flat = [pixel for row in img for pixel in row]
    im.putdata(flat)
    im.save(path)


def log_transform(img, c=45):
    return [[int(c * math.log(1 + pixel)) for pixel in row] for row in img]


def gamma_transform(img, gamma=0.5, c=1):
    return [[int(c * ((pixel / 255) ** gamma) * 255) for pixel in row] for row in img]


def image_negative(img):
    return [[255 - pixel for pixel in row] for row in img]


def nn_resize(img, new_w, new_h):
    old_h, old_w = len(img), len(img[0])
    result = [[0] * new_w for _ in range(new_h)]
    for i in range(new_h):
        for j in range(new_w):
            old_i = int(i * old_h / new_h)
            old_j = int(j * old_w / new_w)
            result[i][j] = img[old_i][old_j]
    return result


def bilinear_resize(img, new_w, new_h):
    old_h, old_w = len(img), len(img[0])
    result = [[0] * new_w for _ in range(new_h)]
    for i in range(new_h):
        for j in range(new_w):
            x = i * (old_h - 1) / (new_h - 1)
            y = j * (old_w - 1) / (new_w - 1)
            x0, y0 = int(x), int(y)
            x1 = min(x0 + 1, old_h - 1)
            y1 = min(y0 + 1, old_w - 1)
            dx, dy = x - x0, y - y0
            val = (img[x0][y0] * (1 - dx) * (1 - dy) +
                   img[x1][y0] * dx * (1 - dy) +
                   img[x0][y1] * (1 - dx) * dy +
                   img[x1][y1] * dx * dy)
            result[i][j] = int(val)
    return result


def get_center_10x10(img):
    center_row = len(img) // 2
    center_col = len(img[0]) // 2
    values = [row[center_col - 5:center_col + 5] for row in img[center_row - 5:center_row + 5]]
    return values


# -------------------------------
# 主程式封裝
# -------------------------------
def process_images(data_path, result_path=None):
    if result_path is None:
        result_path = os.path.join(os.getcwd(), "results")

    # 建立資料夾
    mkdir(result_path)
    orig_path = os.path.join(result_path, "Original")
    mkdir(orig_path)
    enh_paths = {k: os.path.join(result_path, "Enhancement", k) for k in ["Log", "Gamma", "Negative"]}
    for p in enh_paths.values():
        mkdir(p)
    resize_paths = {k: os.path.join(result_path, "Resize", k) for k in ["NN", "Bilinear"]}
    for p in resize_paths.values():
        mkdir(p)

    raw_files = [f for f in os.listdir(data_path) if f.lower().endswith(".raw")][:3]
    bmp_files = [f for f in os.listdir(data_path) if f.lower().endswith((".bmp", ".jpg", ".jpeg"))][:3]
    all_files = raw_files + bmp_files

    if len(all_files) < 6:
        raise FileNotFoundError("Not enough images: need 3 RAW + 3 BMP/JPG")

    sizes = [(128,128),(32,32),(512,512),(1024,512),(256,512)]
    center_pixels_dict = {}
    pil_images = []

    for file in all_files:
        full_path = os.path.join(data_path, file)
        if file.lower().endswith(".raw"):
            img_2d = read_raw_gray(full_path)
            pil_img = Image.new("L", (512,512))
            flat = [pixel for row in img_2d for pixel in row]
            pil_img.putdata(flat)
        else:
            pil_img = Image.open(full_path).convert("L")

        pil_images.append(pil_img)
        # 儲存原圖
        save_image([[pil_img.getpixel((x,y)) for x in range(pil_img.width)] for y in range(pil_img.height)],
                   os.path.join(orig_path, file.split('.')[0]+".png"))

        # 中心像素
        center_pixels_dict[file] = get_center_10x10([[pil_img.getpixel((x,y)) for x in range(pil_img.width)]
                                                     for y in range(pil_img.height)])

        # Enhancement
        img_2d = [[pil_img.getpixel((x,y)) for x in range(pil_img.width)] for y in range(pil_img.height)]
        save_image(log_transform(img_2d), os.path.join(enh_paths["Log"], file.split('.')[0]+"_log.png"))
        save_image(gamma_transform(img_2d), os.path.join(enh_paths["Gamma"], file.split('.')[0]+"_gamma.png"))
        save_image(image_negative(img_2d), os.path.join(enh_paths["Negative"], file.split('.')[0]+"_neg.png"))

        # Resize
        for new_w,new_h in sizes:
            nn_img = nn_resize(img_2d,new_w,new_h)
            bil_img = bilinear_resize(img_2d,new_w,new_h)
            save_image(nn_img, os.path.join(resize_paths["NN"], f"{file.split('.')[0]}_NN_{new_w}x{new_h}.png"))
            save_image(bil_img, os.path.join(resize_paths["Bilinear"], f"{file.split('.')[0]}_Bil_{new_w}x{new_h}.png"))

        img_32x32 = nn_resize(img_2d, 32, 32)
        img_32_to_512 = nn_resize(img_32x32, 512, 512)
        save_image(img_32_to_512, os.path.join(resize_paths["NN"], f"{file.split('.')[0]}_NN_32x32_to_512x512.png"))

        img_32x32 = nn_resize(img_2d, 32, 32)
        img_32_to_512 = nn_resize(img_32x32, 512, 512)
        save_image(img_32_to_512, os.path.join(resize_paths["Bilinear"], f"{file.split('.')[0]}_Bilinear_32x32_to_512x512.png"))

    # 儲存中心10x10文字檔
    with open(os.path.join(result_path, "center_pixels.txt"), "w") as f:
        for file,pixels in center_pixels_dict.items():
            f.write(f"{file}:\n")
            for row in pixels:
                f.write(" ".join(map(str,row)) + "\n")
            f.write("\n")

    # 合併 6 張縮圖成 2x3 大圖
    thumbs = [img.resize((128,128)) for img in pil_images]
    merged = Image.new("L",(128*3,128*2))
    for idx,thumb in enumerate(thumbs):
        x = (idx%3)*128
        y = (idx//3)*128
        merged.paste(thumb,(x,y))
    merged_path = os.path.join(result_path,"merged_original.png")
    merged.save(merged_path)

    # 第一張縮圖
    first_thumb_path = os.path.join(result_path,"first_thumb.png")
    thumbs[0].save(first_thumb_path)

    return pil_images, merged_path, first_thumb_path, result_path


# -------------------------------
# GUI 主視窗
# -------------------------------
def run_gui():
    def select_folder():
        folder = filedialog.askdirectory()
        folder_path.set(folder)

    def run_processing():
        folder = folder_path.get()
        if not folder:
            messagebox.showwarning("Warning", "Please select dataset folder first!")
            return

        btn_run.config(state="disabled")
        status_label.config(text="Processing, please wait...")

        def task():
            try:
                images, merged_path, first_thumb_path, result_path = process_images(folder)
                status_label.config(text=f"Completed! Results in {result_path}")

                canvas.delete("all")
                canvas.images = []

                # 顯示合併圖
                merged_img = Image.open(merged_path)
                tk_merged = ImageTk.PhotoImage(merged_img)
                canvas.create_image(0,0,anchor="nw",image=tk_merged)
                canvas.images.append(tk_merged)

                # 顯示第一張縮圖
                first_thumb = Image.open(first_thumb_path)
                tk_first = ImageTk.PhotoImage(first_thumb)
                canvas.create_image(400,0,anchor="nw",image=tk_first)
                canvas.images.append(tk_first)

            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                btn_run.config(state="normal")

        threading.Thread(target=task).start()

    root = tk.Tk()
    root.title("Image Processing Tool")

    folder_path = tk.StringVar()
    tk.Label(root,text="Select Dataset Folder:").grid(row=0,column=0,padx=5,pady=5)
    tk.Entry(root,textvariable=folder_path,width=50).grid(row=0,column=1,padx=5,pady=5)
    tk.Button(root,text="Browse",command=select_folder).grid(row=0,column=2,padx=5,pady=5)

    btn_run = tk.Button(root,text="Run",command=run_processing,width=20,height=2)
    btn_run.grid(row=1,column=0,columnspan=3,padx=5,pady=10)

    status_label = tk.Label(root,text="Waiting...",fg="blue")
    status_label.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

    canvas = tk.Canvas(root,width=600,height=300,bg="white")
    canvas.grid(row=3,column=0,columnspan=3)
    canvas.images = []

    root.mainloop()


# -------------------------------
# 可獨立執行
# -------------------------------
if __name__ == "__main__":
    run_gui()