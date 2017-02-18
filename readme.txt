Programmer: Tyler Stickler

Program description: This program takes can do two things. It can encode a message into a picture or it can decode a message that is already encoded. The user can decide which option to use by specifying their arguments in the command line. 

Program Execution: There are two options of execution, encoding and decoding. Run the driver file and add the flags needed for encoding or decoding. Encoding requires -i, -o, -e. Decoding requires -d. Using -h or --help will  give further information on the arguments.

	Encoding: python3 driver.py -i <path to image> -o <name of output file> -e <message>
		Note: To encode source code, follow -e with "`<cat pathToFile1 pathToFile2...>`"
			ex. -e "`<cat encode.py decode.py driver.py>`"
	Decoding: python3 driver.py -d <path to image>