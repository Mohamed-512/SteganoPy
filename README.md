# SteganoPy
***This script requires Pillow library to be installed***


A python script that allows you to hide a text in an image, or decode an encrypted image.
  This method works by setting the least significant bits of each color element in each pixel,
to a value that corresponds to the text given when encoding, and reading the least significant 
bits and assembling them to come up with ascii text when decoding.


available funtions: encode & decode
Example: SteganoPy -e ~/Documents/toBeDecoded.png "This is a secret message"

Possible arguments:

encoding => 'Steganography.py  -e  ORIGINAL_IMAGE_PATH  MESSAGE_TO_BE_HIDDEN  [*DECODED_IMAGE_PATH*]'

decoding => 'Steganography.py  -d  DECODED_IMAGE_PATH'

for help => '--help'



***Try fetching the hidden message in the image below using SteganoPy!***
![alt text](https://github.com/MA-Tex/SteganoPy/blob/master/encoded_SteganoPy%20Image.png)
