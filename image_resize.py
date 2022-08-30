from ast import Str
from re import T
from PIL import Image
import os
from os import walk, makedirs, mkdir
from tensorflow.keras.utils import img_to_array

SHOULD_SAVE = True
selected_input = 0

def saveImage(pil_image,prefix_name):
    '''Takes a pillow image instance and a prefix string to save an image, returns img_to_array(new images)'''
    try:
        [name, exten] = pil_image.filename.split('\\')[-1].split('.')
        pil_image.save("{}_{}.{}".format(prefix_name,name, exten))
    except:
        pil_image.save("{}_new_image.jpg".format(prefix_name))
    
    print("image: {} saved".format(prefix_name))


def resizeImageMantainAspect(image_path: Str ,width: int, height: int, background_color: tuple):
    '''Takes a file path , a new width , a new height and a tuple compose of integers (int, int, int) values that represents RGB values , creates a new image with the new width and height but maintains the aspect ratio of the original images pased on the file path , its uses pads of the color on the tuple, returns img_to_array(new images) '''
    image = Image.open(image_path)
    image.thumbnail((width, height), Image.LANCZOS)
    n_width, n_height = image.size
    
    if n_width == n_height:
        return image
    else:
        result = Image.new(image.mode, (width, height), background_color)
        result.paste(image, ((width - n_width) // 2, (height - n_height) // 2))
    
    if SHOULD_SAVE:
        saveImage(result, "padded")

    return img_to_array(result)


def resizeImage(image_path, width, height):
    '''Takes the file path to an image ,a new width and height , rezises the image with the \"width\" and \"height\", returns img_to_array(new images)'''
    image = Image.open(image_path)
    new_image = image.resize((width, height))

    if SHOULD_SAVE:
        saveImage(image, "normal")
        saveImage(new_image, "resize")

    return img_to_array(new_image)


def toGreyScale(image_path):
    '''Takes the file path to an image and creates a greyscale version of the image, returns img_to_array(new images)'''
    image = Image.open(image_path)
    greyscale_image = image.convert('L')
    
    if SHOULD_SAVE:
        saveImage(greyscale_image, "greyscale")
    
    return img_to_array(greyscale_image)


#delete if you dont need the console version
while int(selected_input) != 4:
    print("Please select an option to apply to an image")
    print("1) Image resize")
    print("2) Image resize with aspect")
    print("3) Grey scale")
    print("4) Exit")

    selected_input = input()

    if int(selected_input) == 1:
        print("Please insert the file path:")
        image_path = input()
        print("Select a height")
        height = input()
        print("Select a width")
        width = input()

        try:
            int(height)
            int(width)
        except ValueError as e:
            print("Sorry but {} X {} is not a valid size,use integer numbers: {}".format(width, height, e))
            continue

        try:
            resizeImage(image_path,int(width),int(height))
        except FileNotFoundError as e:
            print(e)
            continue

    if int(selected_input) == 2:
        print("Please insert the file path:")
        image_path = input()
        print("Select a height")
        height = input()
        print("Select a width")
        width = input()
        print("Select a R")
        R = input()
        print("Select a G")
        G = input()
        print("Select a B")
        B = input()

        resizeImageMantainAspect(image_path,int(width),int(height), (int(R),int(G),int(B)))

    if int(selected_input) == 3:
        print("Please insert the file path:")
        image_path = input()
        toGreyScale(image_path)

print("Bye")