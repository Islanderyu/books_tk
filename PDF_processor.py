import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import Image  
import os
import sys

def pdf_to_jpg(pdf_file, output_dir, output_file_prefix, pages,directory):
    # Convert the PDF to a list of PIL images
    Image.MAX_IMAGE_PIXELS = 1000000000
    images = convert_from_path(pdf_file, dpi=200)
    print("PDF讀取完成")
    num_pages = len(images)
    for i, page in enumerate(pages):
        if page >= num_pages:
            print("Error: page {} is out of range (the PDF has {} pages)".format(page, num_pages))
            continue
        # Select the specified page from the PDF
        image = images[page-1]
        # 確認頁碼問題的測試程式
            # print ("image={} page = {}".format(image,page))
        
        # Resize the image to have a width of 1000 while preserving aspect ratio
        image.thumbnail((1000, 1000))
        # Save the selected page as a JPG image
        image.save(os.path.join(output_dir, "{}_b{}.jpg".format(output_file_prefix, i+1)))
        
    # 儲存目錄（但要作判斷）
    if directory:
        image = images[directory-1]
        image.thumbnail((1000, 1000))
        # 儲存目錄圖檔
        image.save(os.path.join(output_dir, "{}_bi.jpg".format(output_file_prefix)))
    else:
        print("沒有選擇目錄頁碼")


def jpg_rename_resize(jpg_file, output_dir, output_file_prefix,cover_or_back):
    # Convert the PDF to a list of PIL images
    Image.MAX_IMAGE_PIXELS = 1000000000
    image = Image.open(jpg_file)
    # Resize the image to have a width of 1000 while preserving aspect ratio
    image.thumbnail((1000, 1000))

    if cover_or_back == "cover":
        # Save the selected page as a JPG image
        image.save(os.path.join(output_dir, "{}_bc.jpg".format(output_file_prefix)))
    else :
        image.save(os.path.join(output_dir, "{}_bf.jpg".format(output_file_prefix)))



# 打開介面，選擇封面圖檔
root = tk.Tk()
root.withdraw()
jpg_file_cover = filedialog.askopenfilename(title="選擇封面圖檔", filetypes=(("JPG圖檔", "*.jpg"), ("All Files", "*.*")))

if not jpg_file_cover:
    print("沒有選擇封面圖檔，程式取消")
    sys.exit()

# 打開介面，選擇封底圖檔
root = tk.Tk()
root.withdraw()
jpg_file_bottom = filedialog.askopenfilename(title="選擇封底圖檔", filetypes=(("JPG圖檔", "*.jpg"), ("All Files", "*.*")))

if not jpg_file_bottom:
    print("沒有選擇封底圖檔，程式取消")
    sys.exit()

# 打開介面，選擇 PDF 檔案
root = tk.Tk()
root.withdraw()
pdf_file = filedialog.askopenfilename(title="選擇PDF檔案", filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")))
if not pdf_file:
    print("PDF file selection cancelled.")
    sys.exit()

# Create a GUI window to select the output directory
output_dir = filedialog.askdirectory(title="選擇儲存路徑",parent=root,
                                    initialdir='~/')

if not output_dir:
    print("Output directory selection cancelled.")
    sys.exit()

# Get the desired prefix for the output JPG files
output_file_prefix = input("請輸入ISBN: ")

# Create the subfolder for the output JPG files
subfolder = os.path.join(output_dir, output_file_prefix)
os.makedirs(subfolder, exist_ok=True)

# Get the list of page numbers to be converted
pages = list(map(int, input("請輸入想要轉換的頁碼（請以半型逗號分隔）: ").strip().split(",")))

# 選擇目錄
directory = int(input("請輸入目錄頁碼:"))
print(directory)

# Convert the selected PDF to JPG and save in the specified directory
pdf_to_jpg(pdf_file, subfolder, output_file_prefix, pages,directory)

# 將封面圖檔轉為指定格式與名稱
jpg_rename_resize(jpg_file_cover, subfolder, output_file_prefix,"cover")

# 將封面圖檔轉為指定格式與名稱
jpg_rename_resize(jpg_file_bottom, subfolder, output_file_prefix,"back")

