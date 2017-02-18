###############################################################################
# Programmer: Tyler Stickler                                                  #
# File name: encrypt.py                                                       #
# Description: This program takes can do two things. It can encode a message  #
#              into a picture or it can decode a message that is already      #
#              encoded. The user can decide which option to use by specifying #
#              their arguments in the command line.                           #
###############################################################################

from PIL import Image
import math
import sys
import argparse


###############################################################################
# This function inputs data into an image. It grabs a pixel at a certain xy   #
# coordinate, starting at the bottom right, converts its RGB value into       #
# binary, then modifies the least significant bit to hide our data. This      #
# continues until the whole message is encoded.                               #
#                                                                             #
# Function input: Image object, message to encode, output file                #
# Function returns: None                                                      #
###############################################################################
def encode_message(im, user_message, output_file):
    # User defined message to encrypt
    message = user_message

    # Determines the width and height of the image
    width, height = im.size
    pixels_in_image = width * height

    # Determines message length, zero fills it up to 33
    message_length = len(message)
    binaryMsgLength = bin(message_length)[2:].zfill(33)
    pixels_needed = math.ceil((message_length * 8) / 3)

    # Determines if their are enough pixels in the image to add the message
    if pixels_needed + 11 > pixels_in_image:
        print("Sorry, your image is too small to hold this big of a message.")
        sys.exit()

    # Creates an array to hold binary values of the letters
    messageArray = []

    # Changes each letter to binary, adds it to the message array, and converts
    # it into a string
    for letter in message:
        binaryVal = bin(ord(letter))[2:].zfill(8)
        messageArray.append(binaryVal)
    binaryMessage = "".join(messageArray)

    # The width and height modifiers are used to move us between pixels
    width_mod = 1
    height_mod = 1

    # Determines how many times we need to loop
    times_to_loop = pixels_needed + 11

    # Used as indexes
    length_counter = 32
    letter_counter = 0

    # Loop through and modify the pixels until task is complete
    while times_to_loop > 0:
        # Gets the pixel's RGB values at the current XY coordinate
        r, g, b = im.getpixel((width-width_mod, height-height_mod))

        # Converts the RGB values to their binary representation
        binary_red = list(bin(r)[2:].zfill(8))
        binary_green = list(bin(g)[2:].zfill(8))
        binary_blue = list(bin(b)[2:].zfill(8))

        # Modifies the least significant bit of the RGB value
        if length_counter > 0:
            # Modify the RGB values to insert message length
            binary_red[7] = binaryMsgLength[length_counter]
            length_counter -= 1
            binary_red = int("".join(binary_red), 2)

            binary_green[7] = binaryMsgLength[length_counter]
            length_counter -= 1
            binary_green = int("".join(binary_green), 2)

            binary_blue[7] = binaryMsgLength[length_counter]
            length_counter -= 1
            binary_blue = int("".join(binary_blue), 2)

            im.putpixel((width - width_mod, height - height_mod),
                        (binary_red, binary_green, binary_blue))
        elif times_to_loop > 0:
            # Modify the RGB values to insert our message
            if letter_counter < message_length * 8:
                binary_red[7] = binaryMessage[letter_counter]
                letter_counter += 1

            if letter_counter < message_length * 8:
                binary_green[7] = binaryMessage[letter_counter]
                letter_counter += 1

            if letter_counter < message_length * 8:
                binary_blue[7] = binaryMessage[letter_counter]
                letter_counter += 1

            binary_red = int("".join(binary_red), 2)
            binary_green = int("".join(binary_green), 2)
            binary_blue = int("".join(binary_blue), 2)

            im.putpixel((width - width_mod, height - height_mod),
                        (binary_red, binary_green, binary_blue))

        # Move us to the next pixel in the row
        width_mod += 1
        times_to_loop -= 1

        # If we hit the left side of the picture, move up a row
        if width_mod-1 == width:
            height_mod += 1
            width_mod = 1

    # Save our encoded file with the user specified name and png format
    im.save("{}.png".format(output_file))


###############################################################################
# This function extracts data from an image. It grabs a pixel at a certain xy #
# coordinate, starting at the bottom right, determines the length and content #
# of the message by checking the least significant bit of each RGB value and  #
# translates it into a readable string.                                       #
#                                                                             #
# Function input: Image object                                                #
# Function returns: Decoded message                                           #
###############################################################################
def decode_message(im):
    # Determines the width and height of the image
    width, height = im.size

    # The width and height modifiers are used to move us between pixels
    width_mod = 1
    height_mod = 1

    # The first 11 pixels we'll look at hold the length of our message
    times_to_loop = 11

    # Holds the least significant bit of the RGB values
    length = []

    # This while loop handles the length of the message
    while times_to_loop > 0:
        # Gets the RGB value at a given XY coordinate
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

        # If we hit the left side of the picture, move up a row
        if width_mod - 1 == width:
            height_mod += 1
            width_mod = 1

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

        # If we hit the left side of the picture, move up a row
        if width_mod - 1 == width:
            height_mod += 1
            width_mod = 1

    # Decoded bits are joined into groups of 8, then turned into a character
    # based off of their ascii value.
    decoded_message = []
    i = 0
    while i != num_of_bits_in_msg:
        decoded_message.append(str(chr(int("".join(bits_message[i:i+8]), 2))))
        i += 8

    # Joins our list so it can be displayed as a string
    decoded_message = "".join(decoded_message)
    return decoded_message


def main():
    # Creates a parser to allow us to handle command line arguments
    parser = argparse.ArgumentParser(description="Encode or decode an image")
    parser.add_argument("-d", "--decode", help="file to decode")
    parser.add_argument("-i", "--inFile", help="path to file to encode")
    parser.add_argument("-e", "--encode", help="message to encode")
    parser.add_argument("-o", "--outFile", help="name of new file")
    args = parser.parse_args()

    # If/else statements to determine what the user would like to do.
    # The first one prevents choosing encoding and decoding at the
    # same time. The second uses an input file, a message, and
    # the name of an output file to execute. The third just needs
    # a file to decode. Otherwise, our user has messed up and we exit.
    if args.encode is not None and args.decode is not None:
        print("You need to choose between encoding and decoding!")
        sys.exit()
    elif args.encode is not None and \
        args.inFile is not None and \
            args.outFile is not None and \
            args.decode is None:
        # Sets the file variable to the image the user has entered
        file = args.inFile
        message = args.encode
        output = args.outFile

        # Creates an image object to allow interaction with the user's image
        im = Image.open(file)

        # Encodes the message and saves it
        encode_message(im, message, output)
    elif args.decode is not None and \
        args.encode is None and \
            args.inFile is None and \
            args.outFile is None:
        # Sets the file variable to the image the user has entered
        file = args.decode

        # Creates an image object to allow interaction with the user's image
        im = Image.open(file)

        # Decodes the message and reports it to the user
        print(decode_message(im))
    else:
        print("You messed up somewhere... Try again.")
        sys.exit()

if __name__ == "__main__":
    main()
