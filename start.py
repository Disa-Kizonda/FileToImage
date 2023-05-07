import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import re,struct
def encode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        with open(filepath, "rb") as file:
            file_bytes = file.read()
        file_bytes = struct.pack(">Q", len(file_bytes)) + file_bytes
        num_padding_bytes = 2048 - len(file_bytes) % 2048
        file_bytes += b"\0" * num_padding_bytes
        image = np.frombuffer(file_bytes, dtype=np.uint8).reshape((-1, 2048))
        for i in range(0, image.shape[0], 2048):
            img = Image.fromarray(image[i:i+2048], "L")
            img.save(f"{filepath}.{i//2048}.png")
    print("The files have been successfully encoded!")
def decode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        if not (".0.png" in filepath):
            continue
        image_data = []
        i = 0
        while True:
            split_image_path = filepath[:-6] + "." + str(i) + ".png"
            try:
                image = Image.open(split_image_path)
                image_data.append(np.array(image))
            except:
                break
            i += 1
        image_data = np.concatenate(image_data)
        file_bytes = image_data.tobytes()
        file_size = int.from_bytes(file_bytes[:8], 'big')
        file_bytes = file_bytes[8:file_size+8]
        file_extension = re.search(r"\.[^.]*$", filepath[:-6]).group()
        output_file_path = filepath[:-6][:-len(file_extension)] + file_extension
        with open(output_file_path, "wb") as output_file:
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