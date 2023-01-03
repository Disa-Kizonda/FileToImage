import tkinter as tk
from tkinter import filedialog
from PIL import Image
def encode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        with open(filepath, "rb") as file:
            file_bytes = file.read()
        file_bytes = len(file_bytes).to_bytes(4, 'big') + file_bytes
        lines = [file_bytes[i:i+2048] for i in range(0, len(file_bytes), 2048)]
        image = Image.new("L", (2048, len(lines)))
        image.putdata([b for line in lines for b in line])
        image.save(filepath + ".png")
    print("The files have been successfully encoded!")
def decode_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        image = Image.open(filepath)
        width, height = image.size
        file_bytes = b"".join(bytes([r]) for r in image.getdata())
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
