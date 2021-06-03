import math
import cv2

MAX_CIRCLE_AREA = 20000
INVALID_GAP = -1


def get_smallest_radius(circles):
    radius = MAX_CIRCLE_AREA

    for circle in circles:
        area = cv2.contourArea(circle)
        # Finds radius using formula: sqrt(area/pi)
        current_radius = int(math.sqrt(area / math.pi))
        if current_radius < radius:
            radius = current_radius

    return radius


def get_circle_cord_from_offset(circle, height_offset, width_offset):
    # Formula found in documentation
    # Moment is the recorded position of contour circle
    # Get coordinates using below. Add offset b/c these circles are from cropped img
    moment = cv2.moments(circle)
    cx = int(moment["m10"] / moment["m00"]) + width_offset
    cy = int(moment["m01"] / moment["m00"]) + height_offset

    return cx, cy


def get_circle_coordinates(circles, image):
    circle_center_x_cords, circle_center_y_cords = [], []

    for circle in circles:
        cx, cy = get_circle_cord_from_offset(circle, image.width_offset, image.height_offset)

        circle_center_x_cords.append(cx)
        circle_center_y_cords.append(cy)

    circle_center_x_cords.sort()
    circle_center_y_cords.sort()

    return circle_center_x_cords, circle_center_y_cords


def find_gap_size(circle_center_cords, radius):
    biggest_gap = INVALID_GAP
    # Look for 2 unique circle_center_cord positions so the
    # horizontal/vertical gap between materials can be found
    for x in range(len(circle_center_cords) - 1):
        left_top_circle = circle_center_cords[x]
        right_bottom_circle = circle_center_cords[x + 1]

        # Can't directly check if the two numbers are different. Sometimes the
        # circle_center_cord is off by 1-2 px even though they are on the same
        # row/column. If the difference is greater than the radius, it is guaranteed
        # to be from a unique circle. However, can't use a circle_center_x_cord
        # if it skips a circle. Radius * 4 makes sure it isn't too far
        if radius < (right_bottom_circle - left_top_circle) < (radius * 4):
            left_top_circle += radius
            right_bottom_circle -= radius
            gap = right_bottom_circle - left_top_circle
            if biggest_gap < gap:
                biggest_gap = gap

    return biggest_gap


def get_bound(cord, gap, radius):
    # Subtract 2 radii and gap to move from the center of 1 circle to another
    while 0 < cord:
        cord -= radius
        cord -= gap
        cord -= radius

        # In this case, we went too far left/up
        if cord < radius:
            cord += radius
            cord += gap
            cord += radius
            break
    return cord


def get_top_left_circle(image, radius, circle):
    horizontal_gap = image.get_horizontal_gap()
    vertical_gap = image.get_vertical_gap()

    cx, cy = get_circle_cord_from_offset(circle, image.height_offset, image.width_offset)

    # Using cx and cy coordinates, keep moving to left/top bounds
    cx = get_bound(cx, horizontal_gap, radius)
    cy = get_bound(cy, vertical_gap, radius)

    return cx, cy


def prepare_cropping(circles, image):
    radius = get_smallest_radius(circles)
    circle_center_x_cords, circle_center_y_cords = get_circle_coordinates(circles, image)

    horizontal_gap = find_gap_size(circle_center_x_cords, radius)
    vertical_gap = find_gap_size(circle_center_y_cords, radius)
    image.set_horizontal_gap(horizontal_gap, radius)
    image.set_vertical_gap(vertical_gap, radius)

    x_cord, y_cord = get_top_left_circle(image, radius, circles[0])

    return radius, x_cord, y_cord
