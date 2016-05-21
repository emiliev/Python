def rotate_left(original_image):
    left_rotated_image = []

    for row in range(len(original_image)):
        left_rotated_image.append([])
        current_col = len(original_image) - row - 1
        for col in range(len(original_image[row])):
            pixel = original_image[col][current_col]
            left_rotated_image[row].append(pixel)

    return left_rotated_image


def rotate_right(original_image):
    right_rotated_image = []

    for row in range(len(original_image)):
        right_rotated_image.append([])
        for col in range(len(original_image[row])):
            pixel = original_image[col][row]
            right_rotated_image[row].insert(0, pixel)
    return right_rotated_image


def invert(original_image):
    inverted_image = []

    for row in range(len(original_image)):
        inverted_row = []

        for col in range(len(original_image[row])):
            red, green, blue = original_image[row][col]
            inverted_row.append((255 - red, 255 - green, 255 - blue))

        inverted_image.append(inverted_row)

    return inverted_image


def lighten_pixel(pixel, coef):
    brighter_pixel = []
    for x in range(len(pixel)):
        cur_color = pixel[x] + int(coef * (255 - pixel[x]))
        brighter_pixel.append(cur_color)

    return tuple(brighter_pixel)


def lighten(original_image, coef):
    lightened_image = []

    for row in range(len(original_image)):
        lightened_row = []

        for col in range(len(original_image[row])):
            pixel = original_image[row][col]
            lightened_row.append(lighten_pixel(pixel, coef))

        lightened_image.append(lightened_row)

    return lightened_image


def darken_pixel(pixel, coef):
    dark_pixel = []
    for x in range(len(pixel)):
        cur_color = pixel[x] - int(coef * (pixel[x] - 0))
        dark_pixel.append(cur_color)
    return tuple(dark_pixel)


def darken(original_image, coef):
    darkened_image = []

    for row in range(len(original_image)):
        darkened_row = []

        for col in range(len(original_image[row])):
            pixel = original_image[row][col]
            darkened_row.append(darken_pixel(pixel, coef))

        darkened_image.append(darkened_row)

    return darkened_image


def create_histogram(original_image):
    rgb = ['red', 'green', 'blue']
    histogram = {rgb[i]: {} for i in range(len(rgb))}

    for row in range(len(original_image)):
        for col in range(len(original_image[row])):
            pixel = original_image[row][col]

            for col in range(len(rgb)):
                if pixel[col] in histogram[rgb[col]]:
                    histogram[rgb[col]][pixel[col]] += 1
                else:
                    histogram[rgb[col]][pixel[col]] = 1

    return histogram
