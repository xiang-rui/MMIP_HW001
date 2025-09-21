import os
import math
from PIL import Image
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
    img = Image.open(filename).convert("L")  # 灰階
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
            val = (img[x0][y0] * (1 - dx) * (1 - dy) + img[x1][y0] * dx * (1 - dy) +
                   img[x0][y1] * (1 - dx) * dy + img[x1][y1] * dx * dy)
            result[i][j] = int(val)
    return result


def get_center_10x10(img):
    center_row = len(img) // 2
    center_col = len(img[0]) // 2
    values = [row[center_col - 5:center_col + 5] for row in img[center_row - 5:center_row + 5]]
    return values


# -------------------------------
# 主程式封裝成函數
# -------------------------------
def process_images(data_path, result_path=None):
    """
    data_path: 影像資料集路徑，包含 RAW/BMP 影像
    result_path: 結果資料夾 (若 None 則預設在當前工作目錄)
    """
    if result_path is None:
        result_path = os.path.join(os.getcwd(), "results_no_matplotlib")

    raw_files = [f for f in os.listdir(data_path) if f.lower().endswith(".raw")]
    bmp_files = [f for f in os.listdir(data_path) if
                 f.lower().endswith(".bmp") or f.lower().endswith(".jpg") or f.lower().endswith(".jpeg")]
    all_files = raw_files + bmp_files

    mkdir(result_path)
    mkdir(os.path.join(result_path, "Original"))
    mkdir(os.path.join(result_path, "Enhancement", "Log"))
    mkdir(os.path.join(result_path, "Enhancement", "Gamma"))
    mkdir(os.path.join(result_path, "Enhancement", "Negative"))
    mkdir(os.path.join(result_path, "Resize", "NN"))
    mkdir(os.path.join(result_path, "Resize", "Bilinear"))

    sizes = [(128, 128), (32, 32), (512, 512), (1024, 512), (256, 512)]
    center_pixels_dict = {}

    for file in all_files:
        full_path = os.path.join(data_path, file)

        # 讀影像
        if file.lower().endswith(".raw"):
            img = read_raw_gray(full_path)
        else:
            img = read_bmp(full_path)

        # 儲存原圖
        save_image(img, os.path.join(result_path, "Original", file.split('.')[0] + ".png"))

        # 儲存中心10x10
        center_pixels_dict[file] = get_center_10x10(img)

        # 影像增強
        log_img = log_transform(img)
        gamma_img = gamma_transform(img)
        neg_img = image_negative(img)

        save_image(log_img, os.path.join(result_path, "Enhancement", "Log", file.split('.')[0] + "_log.png"))
        save_image(gamma_img, os.path.join(result_path, "Enhancement", "Gamma", file.split('.')[0] + "_gamma.png"))
        save_image(neg_img, os.path.join(result_path, "Enhancement", "Negative", file.split('.')[0] + "_neg.png"))

        # 下/上採樣
        for new_w, new_h in sizes:
            nn_img = nn_resize(img, new_w, new_h)
            bil_img = bilinear_resize(img, new_w, new_h)
            nn_name = f"{file.split('.')[0]}_NN_{new_w}x{new_h}.png"
            bil_name = f"{file.split('.')[0]}_Bilinear_{new_w}x{new_h}.png"
            save_image(nn_img, os.path.join(result_path, "Resize", "NN", nn_name))
            save_image(bil_img, os.path.join(result_path, "Resize", "Bilinear", bil_name))

    # 儲存中心10x10像素文字檔
    with open(os.path.join(result_path, "center_pixels.txt"), "w") as f:
        for file, pixels in center_pixels_dict.items():
            f.write(f"{file}:\n")
            for row in pixels:
                f.write(' '.join(map(str, row)) + "\n")
            f.write("\n")

    return result_path  # 回傳結果資料夾路徑


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
            messagebox.showwarning("警告", "請先選擇資料集資料夾！")
            return

        btn_run.config(state="disabled")
        status_label.config(text="處理中，請稍候...")

        def task():
            try:
                res_path = process_images(folder)
                status_label.config(text=f"完成！結果已儲存於 {res_path}")
            except Exception as e:
                status_label.config(text=f"發生錯誤: {e}")
            finally:
                btn_run.config(state="normal")

        threading.Thread(target=task).start()

    root = tk.Tk()
    root.title("影像處理工具")

    folder_path = tk.StringVar()

    tk.Label(root, text="選擇資料集資料夾:").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=folder_path, width=50).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="瀏覽", command=select_folder).grid(row=0, column=2, padx=5, pady=5)

    btn_run = tk.Button(root, text="執行處理", command=run_processing, width=20, height=2)
    btn_run.grid(row=1, column=0, columnspan=3, padx=5, pady=20)

    status_label = tk.Label(root, text="等待執行...", fg="blue")
    status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    root.mainloop()


# -------------------------------
# 可獨立執行
# -------------------------------
if __name__ == "__main__":
    run_gui()