import sys
import os
import json

from PIL import Image
import imagehash

import cv2


def init_hashing():
    hashed_images = {}

    directory = '../resources/items/'
    os.chdir(directory)

    for filename in os.listdir():
        item_hash = imagehash.average_hash(Image.open(filename))
        
        split_filename = filename.split(".")[0]
        hashed_images[split_filename] = item_hash

    return hashed_images


def hashing(item_images, hashed_images):
    for item in item_images:
        original_item_hash = imagehash.average_hash(Image.fromarray(item))

        most_similar = 11
        most_similar_item = "Unknown"

        for current_name, current_hash in hashed_images.items():
            similarity_value = current_hash - original_item_hash

            if similarity_value < most_similar:
                most_similar = similarity_value
                most_similar_item = current_name

        cv2.imshow("", item)
        print(most_similar_item)
        print(most_similar)
        cv2.waitKey(0)

    '''
        with open('../items.json') as items_file:
        data = json.load(items_file)

        for item in item_images:
            original_item_hash = imagehash.average_hash(Image.fromarray(item))
            original_item_hash = int(str(original_item_hash), 16)

            most_similar = sys.maxsize
            most_similar_item = ""

            for cached_item in data["items"]:
                current_name = cached_item["name"]
                current_hash = cached_item["hash"]

                # or maybe other way around?)

                similarity_value = original_item_hash - int(current_hash, 16)

                if similarity_value < most_similar:
                    most_similar = similarity_value
                    most_similar_item = current_name

            # after testing, just save it to a directory with the file name
            cv2.imshow("", item)
            print(most_similar_item)
            cv2.waitKey(0)

    '''



# try this maybe for better results?
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
