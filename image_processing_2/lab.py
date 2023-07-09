"""
6.1010 Spring '23 Lab 2: Image Processing 2
"""

#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image

# Pasted from previous lab


def get_pixel(image, row, col, behavior=None):
    """
    return the pixel color number at the given
    point based on row, col, and the behavior
    """
    if 0 <= row < image["height"] and 0 <= col < image["width"]:
        index = image["width"] * (row) + (col)
        return image["pixels"][index]

    elif behavior == "zero":
        return 0

    elif behavior == "extend":
        # if row >= image["height"] and col >= image["width"]:
        #     return get_pixel(image, image["height"] - 1, image["width"] - 1)
        # elif row >= image["height"] and col < 0:
        #     return get_pixel(image, image["height"] - 1, 0)
        # elif row < 0 and col >= image["width"]:
        #     return get_pixel(image, 0, image["width"] - 1)
        # elif row < 0 and col < 0:
        #     return get_pixel(image, 0, 0,)
        if row < 0:
            return get_pixel(image, 0, col, "extend")
        elif row >= image["height"]:
            return get_pixel(image, image["height"] - 1, col, "extend")
        elif col < 0:
            return get_pixel(image, row, 0, "extend")
        elif col >= image["width"]:
            return get_pixel(image, row, image["width"] - 1, "extend")

    elif behavior == "wrap":
        row1 = row
        col1 = col

        if row1 >= image["height"] or row1<0:
            # while row1 >= image["height"]:
            row1 %= image["height"]
        # elif row1 < 0:
            # while row1 < 0:
            # row1 %= image["height"]

        if col1 >= image["width"] or col1<0:
            # while col1 >= image["width"]:
            col1%= image["width"]
        # elif col1 < 0:
        #     # while col1 < 0:
        #     col1 %= image["width"]

        return get_pixel(image, row1, col1)


def set_pixel(image, row, col, color):
    """
    sets the pixel at the given point
    based on row and colto the inputted
    color
    """
    index = image["width"] * (row) + (col)
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
    return apply_per_pixel(image, lambda color: 255 - color)


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
    for i, value in enumerate(nums):
        nums[i] = float(nums[i])

    originrow = int(height / 2)
    origincol = int(width / 2)
    out = []

    for i, value in enumerate(nums):
        y = int(i / width) - originrow
        x = int(i % width) - origincol
        out.append((y, x, value))

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

    The correlate function expects the kernel input to be a list
    containing three things: the string containing all of the multipliers
    in index order, the same as how we index
    in images (each value seperated by a " ") ; the height of the matrix;
    the width of the matrix

    Reasoning for string input: by taking the input as a string, this makes it easy
    for the programmer to copy and paste a matrix without having to enter the commas of
    a list by hand, all they have to do is get rid of the new lines

    example ["0 0 0 0 1 0 0 0 0", 3, 3] denotes the following matrix
    0 0 0
    0 1 0
    0 0 0

    correlate then calls another function, create_kernel, with the following inputs:
    create_kernel(kernel[0],kernel[1],kernel[2])

    The docstring for create_kernel can be consulted for the 
    representation of the values.
    """
    matrix = create_kernel(kernel[0], kernel[1], kernel[2])
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }

    for col in range(image["width"]):
        for row in range(image["height"]):
            color = 0.0
            for i in matrix:
                temprow = row + i[0]
                tempcol = col + i[1]
                temp = get_pixel(image, temprow, tempcol, boundary_behavior)
                temp = temp * i[2]
                color += temp
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
        if value < 0:
            image["pixels"][i] = 0
        elif value > 255:
            image["pixels"][i] = 255

        if isinstance(value, float):
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
    num = 1 / amount
    kernel = ""
    for i in range(amount):
        if i == amount - 1:
            kernel = kernel + str(num)
        else:
            kernel = kernel + str(num) + " "

    # then compute the correlation of the input image with that kernel
    result = correlate(image, [kernel, kernel_size, kernel_size], "extend")
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(result)
    return result


def sharpened(image, n):
    """
    Sharpens image using formuala S = 2I - B
    """

    temp = blurred(image, n)
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }

    for i, value in enumerate(result["pixels"]):
        result["pixels"][i] = 2 * value - temp["pixels"][i]
    round_and_clip_image(result)
    return result


def edges(image):
    """
    Uses edge formula to amplify pixels that have drastic
    color changes
    """
    temp1 = correlate(image, ["-1 -2 -1 0 0 0 1 2 1", 3, 3], "extend")
    temp2 = correlate(image, ["-1 0 1 -2 0 2 -1 0 1", 3, 3], "extend")
    result = {"height": image["height"], "width": image["width"], "pixels": []}

    for i in range(len(temp1["pixels"])):
        result["pixels"].append(
            round(math.sqrt(temp2["pixels"][i] ** 2 + temp1["pixels"][i] ** 2))
        )

    round_and_clip_image(result)
    return result


# VARIOUS FILTERS

def color_image_splitter(image):
    """
    Takes in a color image and returns a list containg greyscale images
    from color values in the format
    [r, g, b]
    """
    red_pixels = []
    green_pixels = []
    blue_pixels = []
    for _, val in enumerate(image["pixels"]):
        red_pixels.append(val[0])
        green_pixels.append(val[1])
        blue_pixels.append(val[2])
    red = {"height": image["height"], "width": image["width"], "pixels": red_pixels}
    green = {"height": image["height"], "width": image["width"], "pixels": green_pixels}
    blue = {"height": image["height"], "width": image["width"], "pixels": blue_pixels}
    return [red, green, blue]

def grey_to_color(r,g,b):
    """
    Takes in three greyscale images corresponding to the red, green, and blue
    values and recombines it to one image
    """
    out = {"height": r["height"], "width": r["width"], "pixels": []}
    for i in range(len(r["pixels"])):
        out["pixels"].append((r["pixels"][i], g["pixels"][i], b["pixels"][i]))

    return out
def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """

    def func(image):
        greys = color_image_splitter(image)
        red,green,blue = greys[0], greys[1],greys[2]
        red = filt(red)
        green = filt(green)
        blue = filt(blue)
        return grey_to_color(red,green,blue)

    return func


def make_blur_filter(kernel_size):
    def func(image):
        return blurred(image, kernel_size)

    return func


def make_sharpen_filter(kernel_size):
    def func(image):
        return sharpened(image, kernel_size)
    return func


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """

    def func(image):
        result = image
        for i in filters:
            result = i(result)
        return result
    return func


# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    current = image
    grey_im = greyscale_image_from_color_image(current)
    for _ in range(ncols):
        seam = minimum_energy_seam(cumulative_energy_map(compute_energy(grey_im)))
        grey_im = image_without_seam(grey_im, seam)
        current = image_without_seam(current, seam)
    return current


# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    pixels = []
    for i in image["pixels"]:
        pixels.append(round(0.299 * i[0] + 0.587 * i[1] + 0.114 * i[2]))
    out = {"height": image["height"], "width": image["width"], "pixels": pixels}
    return out


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    left = (0, 1)
    right = (-1, 0)
    other = (-1, 0, 1)
    pixels = energy["pixels"][:]
    result = {"height": energy["height"], "width": energy["width"], "pixels": pixels}

    for row in range(1, energy["height"]):
        for col in range(energy["width"]):
            temp = []

            if col == 0:
                temp.append(get_pixel(result, row - 1, col + left[0]))
                temp.append(get_pixel(result, row - 1, col + left[1]))

            elif col == energy["width"] - 1:
                temp.append(get_pixel(result, row - 1, col + right[0]))
                temp.append(get_pixel(result, row - 1, col + right[1]))

            else:
                temp.append(get_pixel(result, row - 1, col + other[0]))
                temp.append(get_pixel(result, row - 1, col + other[1]))
                temp.append(get_pixel(result, row - 1, col + other[2]))

            value = get_pixel(result, row, col) + min(temp)
            set_pixel(result, row, col, value)
    return result


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    out = []
    last_row = cem["pixels"][len(cem["pixels"]) - cem["width"] :]
    temp = min(last_row)
    col = last_row.index(temp)
    index = (cem["height"] - 1) * cem["width"] + col
    out.append(index)
    left = (0, 1)
    right = (-1, 0)
    other = (-1, 0, 1)

    for row in range(cem["height"] - 1, 0, -1):
        temp = []
        offset = None
        if col == 0:
            temp.append(get_pixel(cem, row - 1, col + left[0]))
            temp.append(get_pixel(cem, row - 1, col + left[1]))
            offset = left[temp.index(min(temp))]
        elif col == cem["width"] - 1:
            temp.append(get_pixel(cem, row - 1, col + right[0]))
            temp.append(get_pixel(cem, row - 1, col + right[1]))
            offset = right[temp.index(min(temp))]
        else:
            temp.append(get_pixel(cem, row - 1, col + other[0]))
            temp.append(get_pixel(cem, row - 1, col + other[1]))
            temp.append(get_pixel(cem, row - 1, col + other[2]))
            offset = other[temp.index(min(temp))]

        col += offset
        out.append((row - 1) * cem["width"] + col)

    return out


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    pixels = image["pixels"][:]
    for i in seam:
        pixels.pop(i)
    return {"height": image["height"], "width": (image["width"] - 1), "pixels": pixels}


def custom_feature(image, color, multiplier):
    """
    Warm/Cool color amplifier
    Inputs:
    Image: the image you want to apply the filter to

    color: a string representing the type of colors you want to
    target. There are two possibilities for this input
    "cool" and "warm" This tells us what rgb values to target

    multipler: a float that will be added to the 1 for the amount
    target colors will be amplified

    ex. multiplier = .5
    a pixel color of 50 would be multiplied by 1.5 to get 75

    Returns:
    An image with the specified colors amplified
    """
    out = image["pixels"][:]
    if color == "warm":
        for i, _ in enumerate(out):
            value = round(image["pixels"][i][0] * (1 + multiplier))
            value = min(value,255)
            out[i] = (value, image["pixels"][i][1], image["pixels"][i][2])
    elif color == "cool":
        for i, _ in enumerate(out):
            value = round(image["pixels"][i][2] * (1 + multiplier))
            value = min(value,255)
            out[i] = (image["pixels"][i][0], image["pixels"][i][1], value)
    result = {"height": image["height"], "width": image["width"], "pixels": out}
    return result


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
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
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    pass
