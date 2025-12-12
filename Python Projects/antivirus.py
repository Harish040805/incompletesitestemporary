import hashlib
import os
import tkinter as tk
from tkinter import filedialog

def calculate_hash(file_path):
    with open(file_path, 'rb') as file:
        file_hash = hashlib.sha256(file.read()).hexdigest()
    return file_hash

def scan_file(file_path):
    """
    Scan a file for malware signatures.
    """
    file_hash = calculate_hash(file_path)
    for malware, signature in signature_db.items():
        if file_hash == signature:
            print(f"Malware detected:{malware} in file {file_path}")
            return True
    print(f"No Malware detected in the file {file_path}")
    return False

def select_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    
def scan_selected_file():
    file_path = entry.get()
    result = scan_file(file_path)
    result_label.config(text=result)
    
root = tk.Tk()
root.title("Antivirus Scanner")

frame=tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Select file to scan:").pack()
entry = tk.Entry(frame, width=50)
entry.pack()
tk.Button(frame, text="Browse",
command=select_file).pack()

tk.Button(frame, text="Scan",
command=scan_selected_file).pack()
result_label = tk.Label(frame, text="")
result_label.pack()

root.mainloop()