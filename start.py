import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
def encode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        with open(filepath, "rb") as file:
            file_bytes = file.read()
        file_bytes = len(file_bytes).to_bytes(4, 'big') + file_bytes
        lines = [file_bytes[i:i+2048] for i in range(0, len(file_bytes), 2048)]
        image = np.empty((len(lines), 2048), dtype=np.uint8)
        for i, line in enumerate(lines):
            padded_line = np.pad(np.frombuffer(line, dtype=np.uint8), (0, 2048-len(line)), mode="constant")
            image[i] = padded_line
        image = Image.fromarray(image, "L")
        image.save(filepath + ".png")
    print("The files have been successfully encoded!")
def decode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        image = Image.open(filepath)
        width, height = image.size
        image_data = np.array(image.getdata(), dtype=np.uint8)
        file_bytes = image_data.tobytes()
        file_size = int.from_bytes(file_bytes[:4], 'big')
        file_bytes = file_bytes[4:file_size+4]
        with open(filepath[:-4], "wb") as output_file:
            output_file.write(file_bytes)
    print("The files have been successfully decoded!")
root = tk.Tk()
root.title("Encoding/decoding a file")
root.geometry('100x75')
encode_button = tk.Button(text="Encode the file", command=encode_file)
decode_button = tk.Button(text="Decode the file", command=decode_file)
encode_button.pack()
decode_button.pack()
root.mainloop()