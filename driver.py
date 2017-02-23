###############################################################################
# Programmer: Tyler Stickler                                                  #
# File name: driver.py                                                        #
# Description: This program takes can do two things. It can encode a message  #
#              into a picture or it can decode a message that is already      #
#              encoded. The user can decide which option to use by specifying #
#              their arguments in the command line.                           #
###############################################################################

from PIL import Image
import sys
import os
import argparse
import decode
import encode


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

        # Checks to make sure the user has entered a .jpg file to work with
        file_extension = os.path.splitext(file)[1]
        if file_extension != ".jpg":
            print("Sorry, you've entered an invalid file type. Please provide"
                  " a .jpg file to encode.")
            sys.exit()

        # Creates an image object to allow interaction with the user's image
        im = Image.open(file)

        # Encodes the message and saves it
        encode.encode_message(im, message, output)
    elif args.decode is not None and \
        args.encode is None and \
            args.inFile is None and \
            args.outFile is None:
        # Sets the file variable to the image the user has entered
        file = args.decode

        # Creates an image object to allow interaction with the user's image
        im = Image.open(file)

        # Decodes the message and reports it to the user
        print(decode.decode_message(im))
    else:
        print("You messed up somewhere... Try again.")
        sys.exit()

if __name__ == "__main__":
    main()
