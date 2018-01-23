Programmer: Tyler Stickler

Program description: This program can do two things. It can encode a message into an image or it can decode a message that is already encoded into an image. The user can decide which option to use by specifying their arguments in the command line. 

The encoding process works as such: The user chooses any image(input image must be .jpg) and supplies it to the program with a specified name for the output image(output image will be .png) as well as a message they would like to hide in the image. The program will determine the message length and modify the least significant bit of the RGB values of the first 11 pixels, starting in the bottom right corner, to hold the message length. The program will then convert the user message to a string of bits which will also be hidden in the least significant bit of the RGB values beginning at the 12th pixel and continuing until the whole message has been encoded. Finally, a new .png image with the user specified name is created containing the hidden message.

The decoding process works as such: The user specifies an image(.png) they would like to decode. The program will gather the least significant bit of the first 11 pixel's RGB values to determine how long it should decode the message for. Beginning at the 12th pixel, the program will store the least significant bit of each pixel's RGB values until it has reached the message length. Then the program will seperate the bits into groups of eight and convert them into their character representation, which will then be joined to make a string containing the hidden message. This message will then output to the console.

Program Execution: There are two options of execution, encoding and decoding. Run the driver file and add the flags needed for encoding or decoding. Encoding requires -i, -o, -e. Decoding requires -d. Using -h or --help will  give further information on the arguments.

	Encoding: python3 driver.py -i <path to image> -o <name of output file> -e <message>
		Note: To encode source code, follow -e with "`<cat pathToFile1 pathToFile2...>`"
			ex. -e "`cat encode.py decode.py driver.py`"
	Decoding: python3 driver.py -d <path to image>
