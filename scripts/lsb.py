from PIL import Image
import os

def main():

    fileName = input("Enter image name: ")

    if not os.path.exists(fileName):
        print("File doesn't exist")
        return

    color = input("Enter the color you want to extract the LSB from (RGB): ")

    match color:
        case "R":
            colorNumber = 0
        case "G":
            colorNumber = 1
        case "B":
            colorNumber = 2
        case _:
            print("Allowed inputs: \"R\", \"G\" or \"B\"")
            return

    LSBLevel = input("Enter the level of LSB (1-8): ")

    LSBLevel = int(LSBLevel)

    if LSBLevel > 8 or LSBLevel < 1:
        print("LSB level must be within 1-8 range")
        return

    data = imageToBase2(fileName, LSBLevel, colorNumber)

    hexDump = base2ToHex(data)

    if os.path.exists("hex.dump"):
        os.remove("hex.dump")

    f = open("hex.dump", "a")
    f.write(hexDump)
    f.close()
    print("Hex dump in file \"hex.dump\"")
    return

def imageToBase2(fileName, LSBLevel, colorNumber):

    extracted_bin = []

    numberString = "0" * (8 - LSBLevel) + "1" * LSBLevel

    with Image.open(fileName) as img:
        width, height = img.size
        for y in range(0, height):
            for x in range(0, width):
                pixel = list(img.getpixel((x, y)))
                extracted_bin.append(str(format(pixel[colorNumber] & int(numberString, 2),'06b')))

    data = "".join([str(x) for x in extracted_bin])

    return data

def base2ToHex(data):
    hexDump = ""
    i = 4
    while i < len(data) - 4:
        halfByte = data[i - 4 : i]
        match halfByte:
            case "0000":
                hexDump = hexDump + "0"
            case "0001":
                hexDump = hexDump + "1"
            case "0010":
                hexDump = hexDump + "2"
            case "0011":
                hexDump = hexDump + "3"
            case "0100":
                hexDump = hexDump + "4"
            case "0101":
                hexDump = hexDump + "5"
            case "0110":
                hexDump = hexDump + "6"
            case "0111":
                hexDump = hexDump + "7"
            case "1000":
                hexDump = hexDump + "8"
            case "1001":
                hexDump = hexDump + "9"
            case "1010":
                hexDump = hexDump + "A"
            case "1011":
                hexDump = hexDump + "B"
            case "1100":
                hexDump = hexDump + "C"
            case "1101":
                hexDump = hexDump + "D"
            case "1110":
                hexDump = hexDump + "E"
            case "1111":
                hexDump = hexDump + "F"
            case _:
                print("Error while converting to hexadecimal")
                return
        i += 4
    
    return hexDump

if __name__ == "__main__":
    main()
