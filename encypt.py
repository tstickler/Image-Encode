# Library for image modification
from PIL import Image
import os
import math

# Library for argument parsing
import argparse

# User defined message to encrypt
message = "Tyler Stickler"

# Determines message length, zero fills it up to 33
msgLength = len(message)
binaryMsgLength = bin(msgLength)[2:].zfill(33)
pixelsNeeded = math.ceil((msgLength * 8)/3)
print("Pixels Needed:", pixelsNeeded)
print("Message length:", msgLength)
print("Binary Message length:", binaryMsgLength)

# Creates an array to hold binary values of the letters
messageArray = []

# Changes each letter to binary, then adds it to the message array
for letter in message:
    binaryVal = bin(ord(letter))[2:].zfill(8)
    messageArray.append(binaryVal)
binaryMessage = "".join(messageArray)
print("Message:", binaryMessage)

# Sets the file variable to the image the user has entered
file = "zelda.jpg"

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
    lengthCounter = 32
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
        if lengthCounter > 0:
            # Take the least significant bit and modify it according
            binaryRed[7] = binaryMsgLength[lengthCounter]
            lengthCounter -= 1
            binaryRed = int("".join(binaryRed), 2)

            binaryGreen[7] = binaryMsgLength[lengthCounter]
            lengthCounter -= 1
            binaryGreen = int("".join(binaryGreen), 2)

            binaryBlue[7] = binaryMsgLength[lengthCounter]
            lengthCounter -= 1
            binaryBlue = int("".join(binaryBlue), 2)

            im.putpixel((width - widthMod, height - heightMod),
                        (binaryRed, binaryGreen, binaryBlue))
        elif timesToLoop > 0:
            # Modify the RGB to insert our message
            if letterCounter < msgLength * 8:
                binaryRed[7] = binaryMessage[letterCounter]
                letterCounter += 1

            if letterCounter < msgLength * 8:
                binaryGreen[7] = binaryMessage[letterCounter]
                letterCounter += 1

            if letterCounter < msgLength * 8:
                binaryBlue[7] = binaryMessage[letterCounter]
                letterCounter += 1

            binaryRed = int("".join(binaryRed), 2)
            binaryGreen = int("".join(binaryGreen), 2)
            binaryBlue = int("".join(binaryBlue), 2)

            im.putpixel((width - widthMod, height - heightMod),
                        (binaryRed, binaryGreen, binaryBlue))

        # Move us to the next pixel in the row
        widthMod += 1
        timesToLoop -= 1

        # If we hit the left side of the picture, move up a row
        if widthMod-1 == width:
            heightMod += 1
            widthMod = 1


def decryptMessage():
    # The width and height modifiers are used to move us between pixels
    width_mod = 1
    height_mod = 1

    # The first 11 pixels we'll look at hold the length of our message
    times_to_loop = 11

    # Holds the least significant bit of the RGB values
    length = []

    # This while loop handles the length of the message
    while times_to_loop > 0:
        # Gets the RGB value at a given xy coordinate
        r, g, b = im.getpixel((width - width_mod, height - height_mod))

        # Converts the RGB values to binary
        binary_red = list(bin(r)[2:].zfill(8))
        binary_green = list(bin(g)[2:].zfill(8))
        binary_blue = list(bin(b)[2:].zfill(8))

        # Adds the value to our list
        length.append(binary_red[7])
        length.append(binary_green[7])
        length.append(binary_blue[7])

        # Move us to the next pixel in the row
        width_mod += 1
        times_to_loop -= 1

    # Reverses order of the list so bits are in the correct position
    length.reverse()

    # Converts our length to an integer to perform arithmetic
    message_length = int("".join(length), 2)

    # Find out how many bits we need to read
    num_of_bits_in_msg = message_length * 8
    counter = 0

    # Determine the number of pixels to look at for our message
    times_to_loop = math.ceil((num_of_bits_in_msg * 8)/3)

    # List to hold message bits
    bits_message = []

    # This while loop handles the contents of the message
    while times_to_loop > 0:
        # Gets the RGB value at a given xy coordinate
        r, g, b = im.getpixel((width - width_mod, height - height_mod))

        # Converts the RGB values to binary
        binary_red = list(bin(r)[2:].zfill(8))
        binary_green = list(bin(g)[2:].zfill(8))
        binary_blue = list(bin(b)[2:].zfill(8))

        # Here we add the bits of the message to our list. Sometimes,
        # we'll want to stop after the red or green value in order
        # not to grab values unrelated to our message. These if
        # statements allow us to stop if our counter reaches the
        # number of bits in our message.
        if counter < num_of_bits_in_msg:
            bits_message.append(binary_red[7])
            counter += 1
        if counter < num_of_bits_in_msg:
            bits_message.append(binary_green[7])
            counter += 1
        if counter < num_of_bits_in_msg:
            bits_message.append(binary_blue[7])
            counter += 1

        # Move us to the next pixel in the row
        width_mod += 1
        times_to_loop -= 1

    # Bits are grouped joined into groups of 8, then turned into a
    # character based off of their ascii value.
    decoded_message = []
    i = 0
    while i != num_of_bits_in_msg:
        decoded_message.append(str(chr(int("".join(bits_message[i:i+8]), 2))))
        i += 8

    decoded_message = "".join(decoded_message)

# saves our image in png format
# im.save("{}.png".format(fileName))


def main():

    modifyPixel()
    # im.show()
    decryptMessage()

if __name__ == "__main__":
    main()
