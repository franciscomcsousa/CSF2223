from PIL import Image


extracted_bin = []

with Image.open("Dog.png") as img:
    width, height = img.size
    byte = []
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y)))
            # [2:] because we don't want 0b in the file
            extracted_bin.append(bin(pixel[1]&0b00111111)[2:])

data = "".join([str(x) for x in extracted_bin])

f = open("dog", "a")
f.write(data)
f.close()