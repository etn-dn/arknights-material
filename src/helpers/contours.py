import cv2
import imutils

MIN_CIRCLE_AREA = 15000
MAX_CIRCLE_AREA = 20000


def get_circle_contours_from_image(image):
    h_offset = image.height_offset
    w_offset = image.width_offset

    # Crop part of image with white background (Specifically, center of first 2 rows)
    # Need first 2 rows to find gap size between the rows
    cropped_image = image.picture[h_offset: h_offset * 5, w_offset: w_offset * 2]

    # Show the cropped image
    # cv2.imshow("Image", cropped_image)
    # cv2.waitKey(0)

    # Apply negative filter and gray scale
    negative_image = cv2.bitwise_not(cropped_image)
    grayscale_image = cv2.cvtColor(negative_image, cv2.COLOR_BGR2GRAY)
    # WHAT DOES THIS DO?
    thresh = cv2.threshold(grayscale_image, 50, 255, cv2.THRESH_BINARY)[1]

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Set contours as tuple
    contours_tuple = imutils.grab_contours(contours)

    # Get the contours about the size of item circle
    circles = []
    for circle_contour in contours_tuple:
        if MIN_CIRCLE_AREA < cv2.contourArea(circle_contour) < MAX_CIRCLE_AREA:
            circles.append(circle_contour)

    return circles


'''
    # helper function to show the contours
    def show_contours(contours, image):
        for c in contours:
            if MIN_CIRCLE_AREA < cv2.contourArea(c) < MAX_CIRCLE_AREA:
                print(cv2.contourArea(c))

                radius = int(math.sqrt(cv2.contourArea(c) / math.pi))

                # compute the center of the contour
                M = cv2.moments(c)
                # print(M)
                cx = int(M["m10"] / M["m00"]) + width_offset
                cy = int(M["m01"] / M["m00"]) + height_offset
                print(cx)
                print(cy)
                # draw the contour and center of the shape on the image
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.circle(image, (cx - radius, cy - radius), 7, (255, 255, 255), -1)
                cv2.putText(image, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # show the image
                cv2.imshow("Image", image)
                cv2.waitKey(0)
    '''
