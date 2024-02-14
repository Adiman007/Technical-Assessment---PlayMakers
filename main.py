#region Imports
from PIL import Image
import numpy as np
#endregion

#region validation functions
def is_size_valid(image):
    """
    Check if the size of the image is valid.

    Parameters:
    image (PIL.Image): The image to check.

    Returns:
    bool: True if the size is valid, False otherwise.
    """
    return image.size == (512, 512)

def is_in_circle(image):
    """
    Check if all pixels outside a given circle in the image are transparent.

    Args:
        image (PIL.Image.Image): The input image.

    Returns:
        bool: True if all pixels outside the circle are transparent, False otherwise.
    """
    # Load the image and convert it to RGBA
    center = (256, 256)
    radius = 256
    rgba_img = image.convert("RGBA")
    width, height = rgba_img.size
    pixels = np.array(rgba_img)
    # Iterate over each pixel
    for y in range(height):
        for x in range(width):
            # Calculate the distance from the pixel to the center of the circle
            dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)

            # Check if the pixel is outside the circle and it's non-transparent
            if dist > radius and pixels[y, x, 3] > 0:
                return False
            
    return True

def is_happy(image):
    """
    Determines if an image gives happy feelings based on its RGB values.

    Args:
        image (PIL.Image.Image): The image to be evaluated.

    Returns:
        bool: True if the image gives happy feelings, False otherwise.
    """

    rgb_image = image.convert('RGB')

    r, g, b = 0, 0, 0
    for color in rgb_image.getdata():
        r += color[0]
        g += color[1]
        b += color[2]
    r /= rgb_image.size[0] * rgb_image.size[1]
    g /= rgb_image.size[0] * rgb_image.size[1]
    b /= rgb_image.size[0] * rgb_image.size[1]

    return r > g and r > b and r+b+g > 300

def check_image(file, format):
    """
    Check if the given image file meets the specified criteria.

    Args:
        file (str): The path to the image file.
        format (str): The format of the image file.

    Returns:
        None
    """
    image = Image.open(file)

    if not is_size_valid(image):
        print('Invalid size')
        return

    if not is_in_circle(image):
        print('The only non-transparent pixels are not within a circle')
        return

    if not is_happy(image):
        print('The colors of the badge do not give a "happy" feeling')
        return

    print('The image is valid')

#endregion
    
#region parallel functions
def change_size_and_format_to_png(file, format):
    """
    Resize the image to 512x512 pixels, remove pixels outside of the circle and convert it to PNG format.

    Args:
        file (str): The path to the image file.
        format (str): The original format of the image.

    Returns:
        None
    """
    image = Image.open(file)
    name = file.split(f".{format}")[0]
    image = image.resize((512, 512))
    image = make_circle(image)
    image.save(f'new_{name}.' + 'png')
    print('new image saved')

def make_circle(image):
    """
    Applies a circular mask to the input image, removing pixels outside the circle.

    Parameters:
    image (PIL.Image.Image): The input image to be processed.

    Returns:
        None
    """
    # Load the image and convert it to RGBA
    center = (256, 256)
    radius = 256
    rgba_img = image.convert("RGBA")
    width, height = rgba_img.size
    pixels = np.array(rgba_img)
    # Iterate over each pixel
    for y in range(height):
        for x in range(width):
            # Calculate the distance from the pixel to the center of the circle
            dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
            
            # Check if the pixel is outside the circle and it's non-transparent
            if dist > radius and pixels[y, x, 3] > 0:
                pixels[y, x, 3] = 0

    image2 = Image.fromarray(pixels)
    return image2
#endregion
    
#region Tests
name = "valid_hearth.png"
change_size_and_format_to_png("cov.jpg", "jpg")
check_image(name, "png")
#endregion
