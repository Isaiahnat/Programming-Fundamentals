"""
6.1010 Spring '23 Lab 1: Image Processing
"""

#!/usr/bin/env python3

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, row, col, behavior=None):
    """
    return the pixel color number at the given
    point based on row, col, and the behavior
    """
    if (0<=row<image["height"] and 0<=col<image["width"]):
        index = image["width"]*(row)+(col)
        return image["pixels"][index]

    elif behavior=="zero":

        return 0

    elif behavior=="extend":

        if row>=image["height"] and col>=image["width"]:
            return get_pixel(image, image["height"]-1,image["width"]-1)
        elif row>=image["height"] and col<0:
            return get_pixel(image,image["height"]-1,0)
        elif row<0 and col>=image["width"]:
            return get_pixel(image,0,image["width"]-1)
        elif row<0 and col<0:
            return get_pixel(image, 0, 0)
        elif row<0:
            return get_pixel(image, 0, col)
        elif row>=image["height"]:
            return get_pixel(image,image["height"]-1, col)
        elif col<0:
            return get_pixel(image, row, 0)
        elif col>=image["width"]:
            return get_pixel(image, row, image["width"]-1)

    elif behavior=="wrap":

        row1 = row
        col1 = col

        if row1>=image["height"]:
            while row1>=image["height"]:
                row1-= image["height"]
        elif row1<0:
            while row1<0:
                row1+= image["height"]

        if col1>=image["width"]:
            while col1>=image["width"]:
                col1-= image["width"]
        elif col1<0:
            while col1<0:
                col1+= image["width"]

        return get_pixel(image, row1, col1)



def set_pixel(image, row, col, color):
    """
    sets the pixel at the given point
    based on row and colto the inputted 
    color
    """
    index = image["width"]*(row)+(col)
    image["pixels"][index] = color


def apply_per_pixel(image, func):
    """
    Applies the given function to each
    pixel
    """
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }
    for col in range(image["width"]):
        for row in range(image["height"]):
            color = get_pixel(image, row, col)
            new_color = func(color)
            set_pixel(result, row, col, new_color)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda color: 255-color)

def create_kernel(numbers, height, width):
    """
    Creates a kernel that can be used as an input value for correlate
    Arguments: 
    numbers - a string of numbers seperated by spaces that will be 
    to create the matrix
    height - an odd number which represents the height of the matrix
    width - an odd number which represents the width of the matrix

    returns:
    a list containing tuples formatted as (y,x,value)
    y - represents the value to add to the current row number to find
    the desired pixel
    x - represents the value to add to the current column number to find
    the desired pixel
    value - the multiplier to be used when the desired pixel is found

    example create_kernel("0 0 0 0 1 0 0 0 0", 3,3) would return
    [(-1, -1, 0.0), (-1, 0, 0.0), (-1, 1, 0.0), (0, -1, 0.0), (0, 0, 1.0), 
    (0, 1, 0.0), (1, -1, 0.0), (1, 0, 0.0), (1, 1, 0.0)]
    """

    nums = numbers.split(" ")
    for i,value in enumerate(nums):
        nums[i] = float(nums[i])

    originrow = int(height/2)
    origincol = int(width/2)
    out = []

    for i, value in enumerate(nums):
        y = int(i/width)-originrow
        x = int(i%width)-origincol
        out.append((y,x,value))

    return out




# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE

    The correlate function expects the kernel input to be a list containing three things:
    the string containing all of the multipliers in index order, the same as how we index
    in images (each value seperated by a " ") ; the height of the matrix; the width of the matrix

    Reasoning for string input: by taking the input as a string, this makes it easy
    for the programmer to copy and paste a matrix without having to enter the commas of
    a list by hand, all they have to do is get rid of the new lines

    example ["0 0 0 0 1 0 0 0 0", 3, 3] denotes the following matrix
    0 0 0 
    0 1 0 
    0 0 0

    correlate then calls another function, create_kernel, with the following inputs:
    create_kernel(kernel[0],kernel[1],kernel[2])
    
    The docstring for create_kernel can be consulted for the representation of the values.
    """
    matrix = create_kernel(kernel[0],kernel[1],kernel[2])
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }

    for col in range(image["width"]):
        for row in range(image["height"]):
            color = 0.0
            for i in matrix:
                temprow = row+i[0]
                tempcol = col+i[1]
                temp = get_pixel(image,temprow,tempcol,boundary_behavior)
                temp = temp*i[2]
                color+=temp
            set_pixel(result, row, col, color)
    round_and_clip_image(result)
    return result





def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    for i, value in enumerate(image["pixels"]):
        if value<0:
            image["pixels"][i] = 0
        elif value>255:
            image["pixels"][i] = 255

        if isinstance(value,float):
            image["pixels"][i] = round(value)



# FILTERS

def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    amount = kernel_size**2
    num = 1/amount
    kernel = ""
    for i in range(amount):
        if i==amount-1:
            kernel = kernel+str(num)
        else:
            kernel = kernel+str(num)+" "

    # then compute the correlation of the input image with that kernel
    result = correlate(image,[kernel,kernel_size,kernel_size],"extend")
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(result)
    return result

def sharpened(image, n):
    """
    Sharpens image using formuala S = 2I - B
    """

    temp = blurred(image,n)
    result = {"height":image["height"],
            "width":image["width"], 
            "pixels":image["pixels"][:]}

    for i, value in enumerate(result["pixels"]):
        result["pixels"][i] = 2*value-temp["pixels"][i]
    round_and_clip_image(result)
    return result

def edges(image):
    """
    Uses edge formula to amplify pixels that have drastic
    color changes
    """
    temp1 = correlate(image,["-1 -2 -1 0 0 0 1 2 1",3,3],"extend")
    temp2 = correlate(image,["-1 0 1 -2 0 2 -1 0 1",3,3],"extend")
    result = {"height":image["height"],
            "width":image["width"], 
            "pixels":[]}

    for i in range(len(temp1["pixels"])):
        result["pixels"].append(round(math.sqrt(temp2["pixels"][i]**2+temp1["pixels"][i]**2)))

    round_and_clip_image(result)
    return result


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # bluegill = load_greyscale_image("test_images/bluegill.png")
    # save_greyscale_image(inverted(bluegill), "inverted_bluegill.png", mode="PNG")
    # test = {"height": 5, "width": 5 ,"pixels": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]}
    # print(get_pixel(test, 6, -3, "extend"))
    # print(createKernel("0 0 0 0 1 0 0 0 0",3,3))
    # pigbird = load_greyscale_image("test_images/pigbird.png")
    # kernel = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    # save_greyscale_image(correlate(pigbird,[kernel,13,13],"zero"), "zeropigbird.png", mode="PNG")
    # save_greyscale_image(correlate(pigbird,[kernel,13,13],"extend"), "extendpigbird.png", mode="PNG")
    # save_greyscale_image(correlate(pigbird,[kernel,13,13],"wrap"), "wrappigbird.png", mode="PNG")
    # cat = load_greyscale_image("test_images/cat.png")
    # save_greyscale_image(blurred(cat,13),"blurredcat.png", mode = "PNG")
    # python = load_greyscale_image("test_images/python.png")
    # save_greyscale_image(sharpened(python,11),"sharppython.png", mode = "PNG")
    # construct = load_greyscale_image("test_images/construct.png")
    # save_greyscale_image(edges(construct),"edgesconstruct.png", mode = "PNG")
    pass
    