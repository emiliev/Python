def gray_pixel(pixel):
    pix = int((pixel[0] + pixel[1] + pixel[2]) / 3)
    return (pix, pix, pix)


def grayscale(function):
    def convert_grayscale(image):
        new_img = [[gray_pixel(pixel) for pixel in row]
                   for row in image]
        return function(new_img)
    return convert_grayscale

@grayscale
def rotate_left(image):
	return list(zip(*image))[::-1]