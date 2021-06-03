from helpers.contours import get_circle_contours_from_image
from helpers.cropimage import crop_items
from helpers.comparehash import init_hashing
from helpers.comparehash import hashing

import cv2

INVALID_GAP = -1


class InventoryImage:
	def __init__(self, picture):
		self.picture = picture
		self.height, self.width, self.color = picture.shape
		self.horizontal_gap = None
		self.vertical_gap = None

		# Offset used to find the start of the cropped portion of the image
		self.height_offset = int(self.height / 8)
		self.width_offset = int(self.width / 3)

	def set_horizontal_gap(self, size, radius):
		# If valid values aren't found, guess the gap size
		if size is INVALID_GAP:
			size = round(radius * 0.47)
		self.horizontal_gap = size

	def set_vertical_gap(self, size, radius):
		# If valid values aren't found, guess the gap size
		if size is INVALID_GAP:
			size = round(radius * 1.13)
		self.vertical_gap = size

	def get_horizontal_gap(self):
		if self.horizontal_gap is None:
			raise Exception('horizontal gap is None')
		return self.horizontal_gap

	def get_vertical_gap(self):
		if self.vertical_gap is None:
			raise Exception('vertical gap is None')
		return self.vertical_gap


def show_all_images(image):
	cv2.imshow("Image", image)
	cv2.waitKey(0)


def main(test):
	test_path = "../resources/test/" + test
	read_picture = cv2.imread(test_path)
	image = InventoryImage(read_picture)
	circles = get_circle_contours_from_image(image)

	#  If at least 1 circle is found in picture, crop the items.
	if circles:
		item_images = crop_items(circles, image)
		hashed_images = init_hashing()
		hashing(item_images, hashed_images)


main('test1.png')
