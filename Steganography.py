from PIL import Image
import numpy as np
import sys
import os.path

MAX_ARGUMENTS_LIMIT = 4
encode_arg = "-e"
decode_arg = "-d"
help_arg = "--help"
help_txt = "SteganoPy is a python script that does Steganography!\n" \
           "Steganography is a way of encrypting messages into media files *ONLY IN (PNG/JPEG)IMAGES HERE*,\n" \
           "this method changes the bits and RGB components in a way it's not obvious to human eye.\n" \
           "          Example: SteganoPy -e ~/Documents/toBeDecoded.png \"This is a secret message\"\n" \
           "Possible arguments:\n" \
           "encoding => '"+os.path.basename(__file__)+" -e ORIGINAL_IMAGE_PATH MESSAGE_TO_BE_HIDDEN [DECODED_IMAGE_PATH]'\n" \
           "decoding => '"+os.path.basename(__file__)+" -d DECODED_IMAGE_PATH'\n" \
           "for help => '--help'\n"


def get_image(image_path):
    im = Image.open(image_path)
    return im


def encode(im, wh_couple, pixels, text):
    written = 0
    char_index = 0
    bit_index = 0

    write_limit = len(text) * 7

    (width, height) = wh_couple
    for w in range(width):
        for h in range(height):
            r, g, b = 0, 0, 0
            for i in range(3):
                color = pixels[w, h][i]
                if written < write_limit:
                    bit = '{0:07b}'.format(ord(text[char_index]))[bit_index]
                    if color % 2 == 0 and bit == "1":
                        color += 1
                    elif color % 2 == 1 and bit == "0":
                        color -= 1
                    bit_index += 1
                    written += 1
                    if bit_index == 7:
                        bit_index = 0
                        char_index += 1
                else:
                    if color % 2 == 1:
                        color -= 1
                if i == 0:
                    r = color
                elif i == 1:
                    g = color
                elif i == 2:
                    b = color
            pixels[w, h] = (r, g, b)

    return np.asarray(im)


def decode(wh_couple, pixels):
    bin_buffer = ""
    something_found = False
    broken = False
    bin_str = ""
    (width, height) = wh_couple

    for w in range(width):
        for h in range(height):
            r, g, b = pixels[w, h]

            bit = "1" if r % 2 == 1 else "0"
            bin_buffer += bit
            if len(bin_buffer) == 7:
                boolean, char = check_bin_buff(bin_buffer)
                if boolean:
                    something_found = True
                    bin_str += char
                else:
                    broken = True
                    break
                bin_buffer = ""

            bit = "1" if g % 2 == 1 else "0"
            bin_buffer += bit
            if len(bin_buffer) == 7:
                boolean, char = check_bin_buff(bin_buffer)
                if boolean:
                    something_found = True
                    bin_str += char
                else:
                    broken = True
                    break
                bin_buffer = ""
            bit = "1" if b % 2 == 1 else "0"
            bin_buffer += bit
           
            if len(bin_buffer) == 7:
                boolean, char = check_bin_buff(bin_buffer)
                if boolean:
                    something_found = True
                    bin_str += char
                else:
                    broken = True
                    break
                bin_buffer = ""

        if broken:
            break

    if something_found:
        return bin_str

    else:
        return None


def check_bin_buff(text):
    char_num = int(text, 2)
    if char_num == 0:
        return False, None
    else:
        return True, chr(char_num)


def encode_operation(path, text, save_path=None):
    original_image_path = path
    new_image_path = "encoded_"+path

    new_image = get_image(original_image_path)
    pixels_rgb, wh = new_image.load(), new_image.size

    if wh[0] * wh[1] * 3 < len(text) * 7:
        print("Warning: Text too long for that image!")

    array = encode(new_image, wh, pixels_rgb, text)
    image = Image.fromarray(array)
    if save_path is None:
        image.save(new_image_path)
    else:
        image.save(save_path)


def decode_operation(path):
    image = get_image(path)
    pixels_rgb, wh = image.load(), image.size
    text_found = decode(wh, pixels_rgb)
    print("Message: " + str(text_found))


def main():
    sys.stdout = sys.stderr
    if len(sys.argv) > MAX_ARGUMENTS_LIMIT + 1:
        print("ERROR: Max number of arguments exceeded!")
    elif len(sys.argv) == 1:
        print("ERROR: Too few arguments!")
        print("_"*100)
        print(help_txt)
    else:
        first_arg = sys.argv[1]
        if first_arg == encode_arg:
            second_arg = sys.argv[2]
            if second_arg == "" or second_arg is None:
                print("ERROR: Too few arguments!")
                return
            image_path = second_arg
            if not (image_path[-3:] != "png" or image_path[-4:] != "jpeg" or image_path[-3:] != "jpg"):
                print("ERROR: Only JPEG & PNG images allowed!")
                return
            elif not os.path.exists(image_path):
                print("ERROR: File not found!")
                return
            else:
                third_arg = sys.argv[3]
                text = third_arg
                if text == "" or text is None:
                    print("ERROR: No text to hide found!")
                    return
                if len(sys.argv) == 4:
                    encode_operation(image_path, str(text))
                elif len(sys.argv) == 5:
                    fourth_arg = sys.argv[4]
                    new_path = fourth_arg
                    if os.access(os.path.dirname(new_path), os.W_OK):
                        encode_operation(image_path, str(text), new_path)
                    else:
                        print("ERROR: Write restricted at '" + new_path + "' or it's a directory!")
                        return
                else:
                    print("ERROR: Too many arguments!")
                    return
        elif first_arg == decode_arg:
            second_arg = sys.argv[2]
            encoded_path = second_arg

            if second_arg == "" or second_arg is None:
                print("ERROR: Too few arguments!")
                return
            elif os.path.exists(encoded_path):
                decode_operation(encoded_path)
            else:
                print("ERROR: File not found!")
                return

        elif first_arg == help_arg:
            print(help_txt)
        else:
            print("ERROR: Unknown or no arguments! "+first_arg)
            return


main()
