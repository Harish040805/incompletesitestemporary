import hashlib
import os
import tkinter as tk
from tkinter import filedialog

signature_db = {
    "Malware1": "malware_signature_1",
    "Malware2": "malware_signature_2"
}

def calculate_hash(file_path):
    file_hash = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(4096):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        print(f"Error reading file: {file_path} - {str(e)}")
        return None

def scan_file(file_path):
    file_hash = calculate_hash(file_path)
    if file_hash is None:
        return None
    for malware, signature in signature_db.items():
        if file_hash == signature:
            return f"Malware detected: {malware} in file {file_path}"
    return "No malware detected"

def select_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def scan_selected_file():
    file_path = entry.get()
    result = scan_file(file_path)
    if result is None:
        result_label.config(text="Error scanning file")
    else:
        result_label.config(text=result)

root = tk.Tk()
root.title("Antivirus Scanner")
root.geometry("1520x760")  # Set the window size

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Select a specific file to scan:").pack()
entry = tk.Entry(frame, width=70, font=('Arial', 12))  # Increased width and font size
entry.pack(pady=10)
tk.Button(frame, text="Browse", command=select_file, font=('Arial', 12)).pack(pady=5)
tk.Button(frame, text="Scan Selected File", command=scan_selected_file, font=('Arial', 12)).pack(pady=5)
result_label = tk.Label(frame, text="", wraplength=450, font=('Arial', 12), justify='left')  # Increased font size
result_label.pack(pady=20)

root.mainloop()