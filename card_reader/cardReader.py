import numpy as np
import cv2
import json
import pytesseract
import os
from os import walk
import shutil
import Sql
import PIL

pytesseract.pytesseract.tesseract_cmd = r'C:\\program Files\\Tesseract-OCR\\tesseract.exe'

card_directory = 'card_reader/new_cards/'
set_directory = 'card_reader/sets/'


def remove_mana(img):

    running = True
    position = 0.0
    while running:
        cropped_image = image_percent_crop(img, position, position+.05, 0, 1)
        height, width, channels = cropped_image.shape
        grey = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        # cv2.imshow('cropped header',grey)

        # get the average
        mean = 0
        for x in range(width):
            for y in range(height):
                mean = mean + grey[y][x]
        mean = int(mean/(width*height))

        # get the variance
        variance = 0
        for x in range(width):
            for y in range(height):
                point = grey[y][x]
                variance = variance + ((point-mean)*(point-mean))
                # print(variance)
        variance = int(variance/(width*height -1))

        if variance < 500:
            running = False
        else:
            position = position + .025

        # print('VARIANCE: ',variance)

    cropped_image = image_percent_crop(img, 0, position+0.02, 0, 1)
    # cv2.imshow('cropped header',cropped_image)

    return cropped_image


def image_percent_crop(img, x_start_percent, x_end_percent, y_start_percent, y_end_percent):
    height, width, channels = img.shape

    x_start = int( width * x_start_percent )
    x_end = int( width * x_end_percent )
    y_start = int( height * y_start_percent )
    y_end = int( height * y_end_percent )

    return img[y_start:y_end, x_start: x_end]


def read_card_image(image_path):
    img = cv2.imread(image_path)

    height, width, channels = img.shape

    # get header image
    header_x_start = .07
    header_x_end = .933
    header_y_start = .023
    header_y_end = .072

    h = 265
    w = 370

    height, width, channels = img.shape
    # print('image dimensions', height, width, channels)
    img = cv2.resize(img, (h, w), interpolation=cv2.INTER_AREA)
    # cv2.imshow('img', img)

    header = image_percent_crop(img, header_x_start, header_x_end, header_y_start,header_y_end)
    header = cv2.blur(header, (2, 2))
    # cv2.imshow('image', header)
    # cut off mana symbols
    cut_image = remove_mana(header)
    # cv2.imshow('mana', cut_image)
    # cv2.waitKey(0)

    text = pytesseract.image_to_string(cut_image)
    # print('precut text: ', text)
    text = text[0:len(text)-1]

    return text


def get_all_cards():
    with open('card_reader/AllPrintings.json', 'r', encoding="utf8") as myfile:
        data = myfile.read()
    # parse file
    return json.loads(data)['data']

    # print(obj['ZEN']['cards'][0].keys())
    # print(cards[0])


def store_card(path, card):
    new_image_name = card['name']

    connection = Sql.get_connection()
    Sql.store_card(card, connection)
    shutil.move(path, 'cards/{}.png'.format(new_image_name))


def run(path):
    completed_cards = []

    filenames = next(walk(path), (None, None, []))[2]  # [] if no file
    #print('FILES: ', filenames)
    for pic in filenames:
        # read in card images from path
        pic_path = path+'/'+pic
        # print('PATH: ',pic_path)
        title = read_card_image(pic_path)
        print('TITLE: ', title)

        img = PIL.Image.open(pic_path)
        img_resized = img.resize((265, 370))
        completed_cards.append({'path': pic_path, 'img': img_resized, 'name':title})

    return completed_cards
# if __name__ == "__main__":
#    main()
