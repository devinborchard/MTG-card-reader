import cv2
import pytesseract
from os import walk
import shutil
import Sql
import PIL

# set the directory for the pytesseract library, this is the default path after installing the library
pytesseract.pytesseract.tesseract_cmd = r'C:\\program Files\\Tesseract-OCR\\tesseract.exe'


# function to find and remove all of the header after the cards name
def remove_mana(img):

    running = True
    position = 0.0

    # loop to run until cutting position is found
    while running:

        # crop the image at the new loop position
        cropped_image = image_percent_crop(img, position, position+.05, 0, 1)

        height, width, channels = cropped_image.shape

        # convert to grey scale for contrast calculations
        grey = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        # get the variance of pixel value to determine if there is still text in the picture
        mean = 0
        for x in range(width):
            for y in range(height):
                mean = mean + grey[y][x]
        mean = int(mean/(width*height))

        variance = 0
        for x in range(width):
            for y in range(height):
                point = grey[y][x]
                variance = variance + ((point-mean)*(point-mean))
                # print(variance)
        variance = int(variance/(width*height -1))

        # once the variance is low enough the mana has been removed
        if variance < 500:
            running = False
        else:
            position = position + .025

    # create final image with found positions plus a margin
    cropped_image = image_percent_crop(img, 0, position+0.02, 0, 1)

    return cropped_image


# function to crop an image to a percent of what it was given x and y start and end percentages
def image_percent_crop(img, x_start_percent, x_end_percent, y_start_percent, y_end_percent):
    height, width, channels = img.shape

    # get the pixel values to start and end at from the percentages of the crops and the image size
    x_start = int(width * x_start_percent)
    x_end = int(width * x_end_percent)
    y_start = int(height * y_start_percent)
    y_end = int(height * y_end_percent)

    # return the new image
    return img[y_start:y_end, x_start: x_end]


# read in a cards image from its path
def read_card_image(image_path):
    # get the original image with cv2 imread function
    img = cv2.imread(image_path)

    # set the values to cut the original image to just get the header of the card
    header_x_start = .07
    header_x_end = .933
    header_y_start = .021
    header_y_end = .072

    # set values for the size of the image after resizing
    h = 265
    w = 370

    img = cv2.resize(img, (h, w), interpolation=cv2.INTER_AREA)  # resize the image

    # crop the image to just get the header
    header = image_percent_crop(img, header_x_start, header_x_end, header_y_start,header_y_end)
    header = cv2.blur(header, (2, 2))  # blur the header so that tesseract library can read the text
    cut_image = remove_mana(header)  # cut off mana symbols
    text = pytesseract.image_to_string(cut_image)  # read text using tesseract
    text = text[0:len(text)-1]  # remove random blank space that always appears after tesseract readings

    return text


# function to store the cards read in to the database using the SQL functions
def store_card(path, card):
    new_image_name = card['name']

    connection = Sql.get_connection()
    Sql.store_card(card, connection)
    shutil.move(path, 'cards/{}.png'.format(new_image_name))


# entry point of file
def run(path):
    completed_cards = []  # create container for cards that get read

    filenames = next(walk(path), (None, None, []))[2]  # [] if no file
    for pic in filenames:
        # read in card images from path
        pic_path = path+'/'+pic

        title = read_card_image(pic_path)
        print('TITLE: ', title)

        img = PIL.Image.open(pic_path)  # read image with PIL
        img_resized = img.resize((265, 370))  # resize image

        # create card object containing the images path, the image, adn the cards name
        completed_cards.append({'path': pic_path, 'img': img_resized, 'name': title})

    return completed_cards
