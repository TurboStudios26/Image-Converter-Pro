# Image Converter Pro - A simple and efficient image format converter built with Python and Tkinter.
# This application allows users to convert images between various formats such as PNG, JPG, JPEG, WEBP, ICO, SVG, BMP, and TIFF.
# Developed by Turbo Studios, this tool is designed to be user-friendly and fast, making it easy for anyone to convert their images with just a few clicks.
# Features:
# - Support for multiple image formats
# - Progress bar to indicate conversion status
# - Error handling to manage unsupported formats or conversion issues

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import aspose.words as aw
import os
import threading
import time

# Format

def process_conversion():
    file_path = filedialog.askopenfilename(
        title="Please select an image file to convert",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff"), ("All Files", "*.*")]
    )
    
    if not file_path:
        return

    convert_btn.config(state="disabled")
    status_label.config(text="Converting...", fg="#555")
    
    thread = threading.Thread(target=run_conversion, args=(file_path,))
    thread.start()

def run_conversion(file_path):
    target_format = format_var.get().lower()
    base_name = os.path.splitext(file_path)[0]
    output_path = f"{base_name}_converted.{target_format}"

    try:
        # প্রগ্রেস বার অ্যানিমেশন
        for i in range(1, 11):
            progress_bar["value"] = i * 10
            root.update_idletasks()
            time.sleep(0.05)

        if target_format == "svg":
            doc = aw.Document()
            builder = aw.DocumentBuilder(doc)
            builder.insert_image(file_path)
            doc.save(output_path)
        else:
            img = Image.open(file_path)
            if target_format in ["jpg", "jpeg"]:
                img = img.convert("RGB")
            
            if target_format == "ico":
                img.save(output_path, format='ICO', sizes=[(64, 64), (128, 128)])
            else:
                img.save(output_path)

        status_label.config(text="Conversion complete! File saved.", fg="green")
        messagebox.showinfo("Success", "Your image has been converted successfully!")

    except Exception as e:
        status_label.config(text="Sorry, an error occurred!", fg="red")
        messagebox.showerror("Error", str(e))
    
    finally:
        convert_btn.config(state="normal")
        progress_bar["value"] = 0

# --- GUI ডিজাইন ---
root = tk.Tk()
root.title("Image Converter Pro")
root.geometry("400x420")
root.configure(bg="#ffffff")

# অ্যাপ টাইটেল
tk.Label(root, text="Image Converter", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333").pack(pady=20)

# ফরম্যাট সিলেকশন বক্স
tk.Label(root, text="Select Format:", bg="#ffffff", font=("Arial", 10)).pack()
format_var = tk.StringVar(value="PNG")
format_options = ["PNG", "JPG", "JPEG", "WEBP", "ICO", "SVG", "BMP", "TIFF"]
dropdown = ttk.Combobox(root, textvariable=format_var, values=format_options, state="readonly", width=15)
dropdown.pack(pady=10)

# প্রগ্রেস বার
progress_bar = ttk.Progressbar(root, orient="horizontal", length=280, mode="determinate")
progress_bar.pack(pady=15)

# স্ট্যাটাস মেসেজ
status_label = tk.Label(root, text="Waiting...", font=("Arial", 9), bg="#ffffff", fg="#888")
status_label.pack()

# বড় কনভার্ট বাটন
convert_btn = tk.Button(root, text="SELECT & CONVERT", command=process_conversion, 
                        bg="#007BFF", fg="white", font=("Arial", 11, "bold"), 
                        padx=30, pady=12, relief="flat", cursor="hand2")
convert_btn.pack(pady=25)

# --- আপনার ব্র্যান্ডিং এরিয়া (অ্যাপের নিচে) ---
footer_frame = tk.Frame(root, bg="#f1f1f1", height=60) # নিচের জন্য আলাদা সেকশন
footer_frame.pack(side="bottom", fill="x")

# এখানে আপনার নাম দিন
dev_label = tk.Label(footer_frame, text="Developed by Turbo Studios", 
                     font=("Arial", 10, "italic"), bg="#f1f1f1", fg="#555")
dev_label.pack(pady=(5, 0))

# ভার্সন নম্বর
version_label = tk.Label(footer_frame, text="Version 1.0.0 (Stable)", 
                         font=("Arial", 8), bg="#f1f1f1", fg="#999")
version_label.pack(pady=(0, 5))

root.mainloop()