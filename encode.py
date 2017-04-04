###############################################################################
# Programmer: Tyler Stickler                                                  #
# File name: encode.py                                                        #
# Description: Encodes a user message into an image.                          #
###############################################################################

import math
import sys


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

    # Determines message length in bits, zero fills it up to 32
    bit_size_message_length = len(message) * 8
    binary_msg_length = bin(bit_size_message_length)[2:].zfill(32)
    pixels_needed = math.ceil(bit_size_message_length / 3) + 11

    # Determines if their are enough pixels in the image to add the message
    if pixels_needed > pixels_in_image:
        print("Sorry, your image is too small to hold this big of a message.")
        sys.exit()

    # Creates an array to hold binary values of the letters
    message_array = []

    # Changes each letter to its binary representation, adds it to the message
    # array, and converts it into a string of 0s and 1s
    for letter in message:
        binary_value = bin(ord(letter))[2:].zfill(8)
        message_array.append(binary_value)
    binary_message = "".join(message_array)

    # The width and height modifiers are used to move us between pixels
    width_mod = 1
    height_mod = 1

    # Used as indexes
    length_counter = 0
    letter_counter = 0

    # Loop through and modify the pixels until task is complete
    while pixels_needed > 0:
        # Determines which pixel we are at
        pixel_x = width - width_mod
        pixel_y = height - height_mod

        # Gets the pixel's RGB values at the current XY coordinate
        r, g, b = im.getpixel((pixel_x, pixel_y))

        # Converts the RGB values to their binary representation
        binary_red = list(bin(r)[2:].zfill(8))
        binary_green = list(bin(g)[2:].zfill(8))
        binary_blue = list(bin(b)[2:].zfill(8))

        # Modifies the least significant bit of the RGB value
        if length_counter < 32:
            # Modify the RGB values to insert message length
            binary_red[7] = binary_msg_length[length_counter]
            length_counter += 1
            binary_red = int("".join(binary_red), 2)

            binary_green[7] = binary_msg_length[length_counter]
            length_counter += 1
            binary_green = int("".join(binary_green), 2)

            # Handles hitting the final blue value, shouldn't be modified
            if length_counter == 32:
                binary_blue = b
            else:
                binary_blue[7] = binary_msg_length[length_counter]
                length_counter += 1
                binary_blue = int("".join(binary_blue), 2)

            # Put the modified pixel into the image
            im.putpixel((pixel_x, pixel_y),
                        (binary_red, binary_green, binary_blue))
        elif pixels_needed > 0:
            # Modify the RGB values to insert our message. Sometimes,
            # we'll want to stop after the red or green value in order
            # not to modify values unrelated to our message. These if
            # statements allow us to stop if our counter reaches the
            # number of bits in our message.
            if letter_counter < bit_size_message_length:
                binary_red[7] = binary_message[letter_counter]
                letter_counter += 1

            if letter_counter < bit_size_message_length:
                binary_green[7] = binary_message[letter_counter]
                letter_counter += 1

            if letter_counter < bit_size_message_length:
                binary_blue[7] = binary_message[letter_counter]
                letter_counter += 1

            binary_red = int("".join(binary_red), 2)
            binary_green = int("".join(binary_green), 2)
            binary_blue = int("".join(binary_blue), 2)

            im.putpixel((pixel_x, pixel_y),
                        (binary_red, binary_green, binary_blue))

        # Move us to the next pixel in the row
        width_mod += 1
        pixels_needed -= 1

        # If we hit the left side of the picture, move up a row
        if width_mod-1 == width:
            height_mod += 1
            width_mod = 1

    # Save our encoded file with the user specified name and .png format
    im.save("{}.png".format(output_file))
