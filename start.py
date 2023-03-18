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
        lines = [file_bytes[i:i+2048] for i in range(0, len(file_bytes), 2048)]
        image = np.frombuffer(b"".join(lines), dtype=np.uint8).reshape((len(lines), 2048))
        images = []
        for y in range(0, image.shape[0], 2048):
            for x in range(0, image.shape[1], 2048):
                new_image = image[y:y+2048, x:x+2048]
                images.append(new_image)
        for i, img in enumerate(images):
            img = Image.fromarray(img, "L")
            img.save(filepath + "." + str(i) + ".png")
    print("The files have been successfully encoded!")
def decode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        if not (".0.png" in filepath):
            continue
        image_data = None
        i = 0
        while True:
            split_image_path = filepath[:-6] + "." + str(i) + ".png"
            try:
                image = Image.open(split_image_path)
                if image_data is None:
                    image_data = np.array(image.getdata(), dtype=np.uint8)
                else:
                    image_data = np.concatenate((image_data, np.array(image.getdata(), dtype=np.uint8)))
            except:
                break
            i += 1
        else:
            image = Image.open(filepath)
            image_data = np.array(image.getdata(), dtype=np.uint8)
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