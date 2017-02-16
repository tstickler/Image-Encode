# Library for image modification
from PIL import Image
import os
import math

# Library for argument parsing
import argparse

# User defined message to encrypt
message = "Tyler"

# Determines message length, zero fills it up to 33
msgLength = len(message)
binaryMsgLength = bin(msgLength)[2:].zfill(33)
pixelsNeeded = math.ceil((msgLength * 8)/3)
print(pixelsNeeded)
print("Message length:", binaryMsgLength)

# Creates an array to hold binary values of the letters
messageArray = []

# Changes each letter to binary, then adds it to the message array
for letter in message:
    binaryVal = bin(ord(letter))[2:].zfill(8)
    messageArray.append(binaryVal)
binaryMessage = "".join(messageArray)
print("Message:", binaryMessage)

# Sets the file variable to the image the user has entered
file = "FullSizeRender.jpg"

# Splits the file name from the extension so we can change it to png
fileName, fileExt = os.path.splitext(file)

# Creates an image object to allow us to interact with the user's image
im = Image.open(file)

# Gets the width and height of our image
width, height = im.size


#######################################################################
# This function inputs the data into the image. It grabs a pixel at a #
# certain xy coordinate, starting at the bottom left, converts its    #
# RGB value into binary, then modifies the least significant bit to   #
# hide our data.                                                      #
#######################################################################
def modifyPixel():
    # The width and height modifiers are used to move us between pixels
    widthMod = 1
    heightMod = 1

    # Determines how many times we need to loop
    timesToLoop = pixelsNeeded + 11

    # Used as indexes
    lengthCounter = 0
    letterCounter = 0

    # Loop through and modify the pixels until task is complete
    while timesToLoop > 0:
        # Gets the pixel at the current xy coordinate
        r, g, b = im.getpixel((width-widthMod, height-heightMod))

        # Converts the RGB values to binary
        binaryRed = list(bin(r)[2:].zfill(8))
        binaryGreen = list(bin(g)[2:].zfill(8))
        binaryBlue = list(bin(b)[2:].zfill(8))

        # Fills the pixel with a new RGB value
        if lengthCounter < 33:
            # Take the least significant bit and modify it according
            binaryRed[7] = binaryMsgLength[lengthCounter]
            lengthCounter += 1
            binaryRed = int("".join(binaryRed),2)

            binaryGreen[7] = binaryMsgLength[lengthCounter]
            lengthCounter += 1
            binaryGreen = int("".join(binaryGreen),2)

            binaryBlue[7] = binaryMsgLength[lengthCounter]
            lengthCounter += 1
            binaryBlue = int("".join(binaryBlue),2)

            im.putpixel((width - widthMod, height - heightMod), (binaryRed, binaryGreen, binaryBlue))

            print(bin(binaryRed), bin(binaryGreen), bin(binaryBlue))

        elif timesToLoop > 1:
            # Modify the RGB to insert our message
            binaryRed[7] = binaryMessage[letterCounter]
            letterCounter += 1
            binaryRed = int("".join(binaryRed))

            binaryGreen[7] = binaryMessage[letterCounter]
            letterCounter += 1
            binaryGreen = int("".join(binaryGreen))

            binaryBlue[7] = binaryMessage[letterCounter]
            letterCounter += 1
            binaryBlue = int("".join(binaryBlue))

            im.putpixel((width - widthMod, height - heightMod), (binaryRed, binaryGreen, binaryBlue))

        # Move us to the next pixel in the row
        widthMod += 1
        timesToLoop -= 1

        # If we hit the left side of the picture, move up a row
        if widthMod-1 == width:
            heightMod += 1
            widthMod = 1


# saves our image in png format
# im.save("{}.png".format(fileName))

def main():

    modifyPixel()
    print(int(binaryMsgLength, 2))
    im.show()

if __name__ == "__main__":
    main()
