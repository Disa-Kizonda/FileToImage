import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import re,struct
def encode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        with open(filepath, "rb") as file:
            data = file.read()
            file_bytes = struct.pack(">Q", len(data)) + data
        num_padding_bytes = 2048 - len(file_bytes) % 2048
        image = np.frombuffer(file_bytes + b"\0" * num_padding_bytes, dtype=np.uint8).reshape((-1, 2048))
        for i in range(0, image.shape[0], 2048):
            Image.fromarray(image[i:i+2048], "L").save(f"{filepath}.{i//2048}.png")
    print("The files have been successfully encoded!")
def decode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        if ".0.png" not in filepath:
            continue
        image_data = []
        i = 0
        while True:
            try:
                image_data.append(np.array(Image.open(f"{filepath[:-6]}.{i}.png")))
            except:
                break
            i += 1
        file_bytes = np.concatenate(image_data).tobytes()
        file_size = int.from_bytes(file_bytes[:8], 'big')
        with open(re.sub(r"\.\d+\.png$", "", filepath), "wb") as output_file:
            output_file.write(file_bytes[8:file_size+8])
    print("The files have been successfully decoded!")
root = tk.Tk()
root.title("Encoding/decoding a file")
root.geometry('100x75')
encode_button = tk.Button(text="Encode the file", command=encode_file)
decode_button = tk.Button(text="Decode the file", command=decode_file)
encode_button.pack()
decode_button.pack()
root.mainloop()