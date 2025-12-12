import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from moviepy.editor import VideoFileClip, ImageClip
import imageio
import os
from fpdf import FPDF
from bs4 import BeautifulSoup

root = tk.Tk()
root.title("Universal File Converter")
root.geometry("700x450")
root.resizable(False, False)

title = tk.Label(root, text="Universal File Converter", font=("Arial", 24, "bold"))
title.pack(pady=20)

conversion_frame = tk.Frame(root)
conversion_frame.pack(pady=10)

conversion_type = tk.StringVar()
conversion_type.set("Image-Video")  # default

def set_conversion(conv):
    conversion_type.set(conv)
    toggle_label.config(text=f"Selected: {conv}")

image_video_btn = tk.Button(conversion_frame, text="Image ↔ Video", width=15, font=("Arial", 12),
                            command=lambda: set_conversion("Image-Video"))
image_video_btn.grid(row=0, column=0, padx=10)

video_audio_btn = tk.Button(conversion_frame, text="Video → Audio", width=15, font=("Arial", 12),
                            command=lambda: set_conversion("Video-Audio"))
video_audio_btn.grid(row=0, column=1, padx=10)

image_gif_btn = tk.Button(conversion_frame, text="Image ↔ Gif", width=15, font=("Arial", 12),
                          command=lambda: set_conversion("Image-Gif"))

image_gif_btn.grid(row=0, column=2, padx=10)

pdf_html_btn = tk.Button(conversion_frame, text="PDF ↔ HTML", width=15, font=("Arial", 12),
                         command=lambda: set_conversion("PDF-HTML"))
pdf_html_btn.grid(row=1, column=0, padx=10, pady=10)

text_html_btn = tk.Button(conversion_frame, text="Text ↔ HTML", width=15, font=("Arial", 12),
                          command=lambda: set_conversion("Text-HTML"))
text_html_btn.grid(row=1, column=1, padx=10, pady=10)

toggle_label = tk.Label(root, text=f"Selected: {conversion_type.get()}", font=("Arial", 14))
toggle_label.pack(pady=10)

input_file_path = tk.StringVar()

def browse_input():
    file = filedialog.askopenfilename()
    if file:
        input_file_path.set(file)

tk.Button(root, text="Select Input File", font=("Arial", 12), command=browse_input).pack(pady=5)
tk.Label(root, textvariable=input_file_path, font=("Arial", 10)).pack(pady=5)

def convert():
    input_file = input_file_path.get()
    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    name, ext = os.path.splitext(input_file)
    conv = conversion_type.get()
    try:
        if conv == "Image-Video":
            clip = ImageClip(input_file, duration=3)
            output_file = name + ".mp4"
            clip.write_videofile(output_file, fps=1)

        elif conv == "Video-Audio":
            clip = VideoFileClip(input_file)
            output_file = name + ".mp3"
            clip.audio.write_audiofile(output_file)

        elif conv == "Image-Gif":
            img = Image.open(input_file)
            if ext.lower() in [".gif"]:
                output_file = name + "_frame.png"
                img.seek(0)
                img.save(output_file, format="PNG")
            else:
                output_file = name + ".gif"
                img.save(output_file, format="GIF")

        elif conv == "PDF-HTML":
            try:
                import pdfplumber
            except:
                messagebox.showerror("Error", "pdfplumber is required for PDF to HTML. Install via pip.")
                return
            if ext.lower() == ".pdf":
                import pdfplumber
                pdf = pdfplumber.open(input_file)
                html_content = ""
                for page in pdf.pages:
                    html_content += f"<p>{page.extract_text()}</p>\n"
                output_file = name + ".html"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
            elif ext.lower() == ".html":
                soup = BeautifulSoup(open(input_file, encoding="utf-8"), "html.parser")
                text = soup.get_text()
                output_file = name + ".pdf"
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in text.split("\n"):
                    pdf.multi_cell(0, 10, line)
                pdf.output(output_file)

        elif conv == "Text-HTML":
            if ext.lower() in [".txt"]:
                with open(input_file, "r", encoding="utf-8") as f:
                    text = f.read()
                output_file = name + ".html"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"<html><body><pre>{text}</pre></body></html>")
            elif ext.lower() == ".html":
                soup = BeautifulSoup(open(input_file, encoding="utf-8"), "html.parser")
                text = soup.get_text()
                output_file = name + ".txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)

        messagebox.showinfo("Success", f"Conversion done!\nSaved as: {output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")

tk.Button(root, text="Convert", font=("Arial", 14), command=convert).pack(pady=20)

root.mainloop()