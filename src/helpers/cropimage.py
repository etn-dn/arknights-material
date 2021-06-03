from helpers.navigatecircles import prepare_cropping


def get_square_image(x_cord, y_cord, radius, picture):
    # Crop item image using bounds
    bottom_bound = y_cord - radius
    top_bound = y_cord + radius
    left_bound = x_cord - radius
    right_bound = x_cord + radius

    return picture[bottom_bound:top_bound, left_bound:right_bound]


def get_row_images(x_cord, y_cord, radius, image):
    images = []
    width = image.width
    horizontal_gap = image.get_horizontal_gap()

    while x_cord < width:
        # Get individual item in the row
        images.append(get_square_image(x_cord, y_cord, radius, image.picture))
        x_cord += radius + horizontal_gap + radius

    return images


def crop_items(circles, image):
    # Get square pictures of each individual item in current picture
    radius, x_cord, y_cord = prepare_cropping(circles, image)

    images = []
    height = image.height
    vertical_gap = image.get_vertical_gap()

    while y_cord < height:
        # Gets individual item going row by row
        images += get_row_images(x_cord, y_cord, radius, image)
        y_cord += radius + vertical_gap + radius

    return images
