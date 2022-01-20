import tkinter as tk
import pathlib
from card_reader import cardReader
from tkinter import ttk
from PIL import ImageTk
from Helpers import get_config, save_config
import Sql


# class for adding functions in the New Cards tab
# this tab has functionality for adding new cards to your collection from pictures
class NewCardsTab:

    def __init__(self, tab_control):  # takes the tab control parameter to attack the tab to the main window
        self.frame = ttk.Frame(tab_control)  # create a new frame for the tab
        self.cards_list = []  # container for the cards that get added

        self.config = get_config()  # load in the app configurations

        # set up the widgets
        tk.Label(self.frame, text="New Cards Images Paths").grid(row=0)

        # create entry for the path containing new card images to be read in
        self.entry_folder_path = tk.Entry(self.frame, width=50)
        self.entry_folder_path.insert(0, self.config["new_image_path"])  # set the default value to the saved path
        self.entry_folder_path.grid(row=0, column=1)

        tk.Button(self.frame, text='Save Path', command=self.save_new_image_path).grid(row=1, column=1, sticky=tk.W,
                                                                                       pady=4)
        tk.Button(self.frame, text='Read Cards', command=self.read_cards_in_path).grid(row=2, column=0, sticky=tk.W,
                                                                                       pady=4)
        number_of_new_cards = self.get_number_of_new_cards()

        self.textBox_number_of_new_cards = tk.Label(self.frame,
                                                    text="Currently {} Cards in directory".format(number_of_new_cards))
        self.textBox_number_of_new_cards.grid(row=2, column=1)

        # create the list box to list the names of the new cards that get read in and let the user preview them
        self.listbox = tk.Listbox(self.frame)
        self.listbox.grid(row=3, column=0, sticky=tk.W, pady=4)
        self.listbox.bind('<<ListboxSelect>>', self.select_list_item)

        # create empty image label that will display the images of the cards
        self.image_label = tk.Label(self.frame)
        self.image_label.grid(row=3, column=1, sticky=tk.W, pady=4)

        # add list to keep track of how many copies of each card their are
        self.quantities = []
        self.label_quantity = tk.Label(self.frame, width=5)
        self.label_quantity.grid(row=4, column=1)

        # add buttons to increase or decrease copies of cards
        tk.Button(self.frame, text='add', command=self.add_quantity).grid(row=5, column=1, sticky=tk.W, pady=4)
        tk.Button(self.frame, text='remove', command=self.remove_quantity).grid(row=6, column=1, sticky=tk.W, pady=4)

        # button to save all of the read in cards to the collection database
        tk.Button(self.frame, text='Store Cards', command=self.store_cards).grid(row=4, column=0, sticky=tk.W, pady=4)

    # function to store all of the cards in the database
    def store_cards(self):
        connection = Sql.get_connection()  # connect to SQL server
        for card in self.cards_list:
            # find the cards data from the all printings database
            card_data = Sql.read_query(connection, 'SELECT * FROM mtg.all_printings WHERE name = "'+card['name']+'";')

            # store the data in the collection database
            Sql.store_card(card_data[0], 'mtg.cards', 1, connection)

    # add a copy of a card
    def add_quantity(self):
        selected_indices = self.listbox.curselection()[0]
        cur = self.quantities[selected_indices]+1
        self.quantities[selected_indices] = cur
        self.label_quantity.config(text=str(cur))

    # remove a copy of a card
    def remove_quantity(self):
        selected_indices = self.listbox.curselection()[0]
        cur = self.quantities[selected_indices]-1
        if cur == 0:  # if you remove the last copy of the card remove the card from the list
            self.remove_card()
        else:
            self.quantities[selected_indices] = cur
            self.label_quantity.config(text=str(cur))

    # save the path entered in the entry box to the configuration object
    def save_new_image_path(self):
        path = self.entry_folder_path.get()
        self.config["new_image_path"] = path
        save_config(self.config)  # save the new configurations

        # display the number of cards in the directory
        self.textBox_number_of_new_cards.config(
            text="Currently {} Cards in directory".format(self.get_number_of_new_cards())
        )

    # remove the selected card from the new cards list and remove it from the display list box
    def remove_card(self):
        selected_indices = self.listbox.curselection()[0]
        self.cards_list.pop(selected_indices)
        self.listbox.delete(selected_indices)
        self.quantities.pop(selected_indices)

        # change the selection to the next card once the currently selected card has been removed
        if selected_indices > 0:
            self.listbox.selection_set(selected_indices-1)
        else:
            self.listbox.selection_set(len(self.cards_list) - 1)
        self.update_card_image()  # update the image label to show the new selection

    # get the cards data from the images in the given directory
    def read_cards_in_path(self):
        self.cards_list = cardReader.run(self.entry_folder_path.get())  # pass the images path to the card reader
        for i, card in enumerate(self.cards_list):
            self.listbox.insert(i, card['name'])  # add all the new cards names to the list box
            self.quantities.append(1)  # add only 1 copy of each card by default

        self.listbox.selection_set(0)  # set the list box selection to the first card in the list
        self.update_card_image()  # update the cards image label to the first card in the list

        # add a button to remove unwanted cards from being added to the collection
        tk.Button(self.frame, text='Remove Card', command=self.remove_card).grid(row=3, column=2, sticky=tk.W, pady=4)

    # function to get the amount of cards that are in the new card directory
    def get_number_of_new_cards(self):
        initial_count = 0
        for path in pathlib.Path(self.entry_folder_path.get()).iterdir():
            if path.is_file():
                initial_count += 1
        return initial_count

    # change the image label to display the image of currently selected card
    def update_card_image(self):
        if self.listbox.curselection():  # if there is a card selected
            selected_indices = self.listbox.curselection()[0]

            img = self.cards_list[selected_indices]["img"]  # get image from the cards list data
            img = ImageTk.PhotoImage(img)  # convert image to tkinter image for displaying

            # set image label
            self.image_label.config(image=img)
            self.image_label.image = img

            # update the cards quantities with the image
            self.label_quantity.config(text=str(self.quantities[selected_indices]))

        else:  # if there is no card selected change the image to the default empty image
            img = []
            self.image_label.config(image=img)
            self.image_label.image = img

    # function to run when a new item is selected in the list box
    def select_list_item(self, event):
        # print("print Trigger")
        self.update_card_image()
