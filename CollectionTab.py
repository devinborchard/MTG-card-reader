import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import PIL
import Sql


# class for adding functions in the collection tab
# this tab has functionality for sorting through your collection and creating decks
class CollectionTab:
    def __init__(self, tab_control):  # takes in the tab control as param for attaching widgets to
        self.frame = ttk.Frame(tab_control)  # create a new frame to attach to the tab
        self.cards_list = []  # a list to hold all the cards in the users collection
        self.get_owned_cards()  # run function to fill cards_list variable with cards
        self.current_shown_cards = self.cards_list  # set the currently shown cards in the list to all cards
        self.deck_list = []  # array to hold different decks0000s

        # create different frames for holding widgets for organization
        # create the frames in rows and add them to the main tabs frame
        row1_frame = tk.Frame(self.frame)
        row1_frame.grid(row=0, column=0)

        row2_frame = tk.Frame(self.frame)
        row2_frame.grid(row=1, column=0)

        row3_frame = tk.Frame(self.frame)
        row3_frame.grid(row=2, column=0)

        row4_frame = tk.Frame(self.frame)
        row4_frame.grid(row=3, column=0)

        # entry for the search by name function
        tk.Label(row1_frame, text="Card Name:").grid(row=0, column=0)
        self.entry_card_name = tk.Entry(row1_frame, width=30)
        self.entry_card_name.grid(row=0, column=1)

        # entry for searching by color
        tk.Label(row1_frame, text="Colors:").grid(row=0, column=2)

        # initialize the boolean variables to attach to the check boxes for searching by color
        self.w_check = tk.IntVar()  # white
        self.b_check = tk.IntVar()  # blue
        self.bl_check = tk.IntVar()  # black
        self.r_check = tk.IntVar()  # red
        self.g_check = tk.IntVar()  # green

        # create check box widgets and attach the boolean variables to their values
        tk.Checkbutton(row1_frame, variable=self.w_check, background='#EBE8C2').grid(row=0, column=3)
        tk.Checkbutton(row1_frame, variable=self.b_check, background='#2C20DC').grid(row=0, column=4)
        tk.Checkbutton(row1_frame, variable=self.bl_check, background='black').grid(row=0, column=5)
        tk.Checkbutton(row1_frame, variable=self.r_check, background='#DC2026').grid(row=0, column=6)
        tk.Checkbutton(row1_frame, variable=self.g_check, background='#287D30').grid(row=0, column=7)

        # entry for searching by mana cost
        tk.Label(row1_frame, text="Mana Cost:").grid(row=0, column=8)
        self.entry_mana_cost = tk.Entry(row1_frame, width=2)
        self.entry_mana_cost.grid(row=0, column=9)

        # entry for searching by type
        tk.Label(row2_frame, text="Types:").grid(row=0, column=1)
        self.entry_card_type = tk.Entry(row2_frame, width=15)
        self.entry_card_type.grid(row=0, column=2)

        # entry for searching by key words
        tk.Label(row2_frame, text="Key Words:").grid(row=0, column=3)
        self.entry_key_words = tk.Entry(row2_frame, width=20)
        self.entry_key_words.grid(row=0, column=4)

        # search Button
        tk.Button(row2_frame, text='search', command=self.search_cards).grid(row=0, column=5, sticky=tk.W, pady=4)

        # clear search Button
        tk.Button(row2_frame, text='Clear All', command=self.search_clear).grid(row=0, column=0, sticky=tk.W, pady=4)

        # searching List box
        self.search_list_box = tk.Listbox(row3_frame)
        self.search_list_box.grid(row=0, column=0, sticky=tk.W, pady=4)
        self.search_list_box.bind('<<ListboxSelect>>', self.select_list_item)

        # create the label that will hold the card images when a card is selected
        self.image_label = tk.Label(row3_frame)
        self.image_label.grid(row=0, column=1, sticky=tk.W, pady=4)

        # create the list box to hold cards that are added to a deck
        self.deck_list_box = tk.Listbox(row3_frame)
        self.deck_list_box.grid(row=0, column=2, sticky=tk.W, pady=4)
        self.deck_list_box.bind('<<ListboxSelect>>', self.select_list_item)

        # update the contents of the
        self.update_list_box()

        # add widgets for creating a deck
        deck_info_frame = tk.Frame(row3_frame) # create a new frame for the deck info to align widgets properly
        deck_info_frame.grid(row=0, column=3)

        tk.Label(deck_info_frame, text="Deck Name:").grid(row=0, column=0)

        self.entry_deck_name = tk.Entry(deck_info_frame, width=10)
        self.entry_deck_name.grid(row=1, column=0)

        tk.Button(deck_info_frame, text='Save Deck', command=self.save_deck).grid(row=2, column=0, sticky=tk.W, pady=4)

        tk.Button(row4_frame, text='Add', command=self.add_card).grid(row=0, column=0, sticky=tk.W, pady=4)

    # function to save the cards put in the deck list into a text file
    def save_deck(self):
        with open('decks/'+self.entry_deck_name.get()+'.txt', 'w') as f:
            text = ''
            for card in self.deck_list:
                text = text+card['card'][1]+'|'
            f.write(text)

    # function that takes the selected card from the search list and adds it to the deck list
    def add_card(self):
        if self.search_list_box.curselection():
            selected_indices = self.search_list_box.curselection()[0]
            self.deck_list.append(self.current_shown_cards.pop(selected_indices))
            self.update_list_box()

    # find the image for the currently selected card and display the image in the image label
    def update_card_image(self):
        img = []  # create image container and set it to empty by default
        if self.search_list_box.curselection():  # check if the selection is in the search box
            selected_indices = self.search_list_box.curselection()[0]
            img = self.current_shown_cards[selected_indices]["img"]

        elif self.deck_list_box.curselection():  # check if the image is in the deck box
            selected_indices = self.deck_list_box.curselection()[0]
            img = self.deck_list[selected_indices]["img"]

        # set the image label to the new found image
        self.image_label.config(image=img)
        self.image_label.image = img

    # function to take all of the entered search parameters and query our card collection
    def search_cards(self):
        # get all the parameters
        name = self.entry_card_name.get()
        mana_cost = self.entry_mana_cost.get()
        types = self.entry_card_type.get()
        keywords = self.entry_key_words.get()

        # get multiple values from entries that can get multiple values
        types = self.string_to_array(types)
        keywords = self.string_to_array(keywords)

        # go through our conditions and place them in a list to create a SQL query
        conditions = []
        if name != '':
            conditions.append('name LIKE "%'+name+'%"')
        if mana_cost != '':
            conditions.append('convertedManaCost = "'+mana_cost+'.0"')
        if types != ['']:
            for item in types:
                conditions.append('types LIKE "%'+item+'%"')
        if keywords != ['']:
            for item in keywords:
                conditions.append('text LIKE "%'+item+'%"')
        if self.w_check.get():
            conditions.append('colors LIKE "%W%"')
        if self.g_check.get():
            conditions.append('colors LIKE "%G%"')
        if self.r_check.get():
            conditions.append('colors LIKE "%R%"')
        if self.b_check.get():
            conditions.append('colors LIKE "%U%"')
        if self.bl_check.get():
            conditions.append('colors LIKE "%B%"')

        # use condition list to create query
        condition_str = ''
        if len(conditions) == 1:
            condition_str = conditions[0]
        elif len(conditions) > 1:
            for i in range(len(conditions)-1):
                condition_str = condition_str + conditions[i] + ' AND '
            condition_str = condition_str + conditions[len(conditions)-1]
        else:  # if there are no condition just set the shown cards to all cards in the collection
            self.current_shown_cards = self.cards_list
            self.update_list_box()
            self.update_card_image()
            return

        # run query to find cards
        connection = Sql.get_connection() # create connection to the database
        query = 'SELECT * FROM mtg.cards WHERE '+condition_str+';'

        found_cards = Sql.read_query(connection, query)  # use SQL function to read data with our query
        self.current_shown_cards = []  # create container to hold our new found cards

        # loop to add the associated card image to the card data from database
        for card in found_cards:
            img = []  # create empty container for image
            for loaded_card in self.cards_list:  # loop through the cards that we already loaded earlier
                if loaded_card["card"][1] == card[1]:  # if a card found matches a card loaded
                    img = loaded_card["img"]  # store the previously loaded image in the new container
            self.current_shown_cards.append({"card": card, "img": img})  # add the found cards data and image to list

        self.update_list_box()

    # clear the search parameters
    def search_clear(self):
        print('CLEAR')

    # update the values displayed in the list box to match the list object containing cards
    def update_list_box(self):
        # delete all items in boxes
        self.search_list_box.delete(0, tk.END)
        self.deck_list_box.delete(0, tk.END)

        # add card names to the list boxes
        for i, card in enumerate(self.current_shown_cards):
            self.search_list_box.insert(i, card["card"][1])

        for i, card in enumerate(self.deck_list):
            self.deck_list_box.insert(i, card["card"][1])

    # function to trigger when an item is selected in a list
    def select_list_item(self, event):
        self.update_card_image()

    # load in all cards in the collection from the Database and get their images
    def get_owned_cards(self):
        connection = Sql.get_connection()
        owned_cards = Sql.read_query(connection, 'Select * from mtg.cards;')

        for card in owned_cards:
            name = card[1]
            img = PIL.Image.open('card_reader/imgs/' + name + '.png')  # find image of the owned card
            img_resized = img.resize((265, 370))  # resize the image to fit in the window
            img = ImageTk.PhotoImage(img_resized)  # convert image to a tkinter image

            self.cards_list.append({"card": card, "img": img})  # add image data and image to list

    # helper function to convert a string of items separated by commas to a list of items
    def string_to_array(self, string):
        if ',' in string:
            array = []
            word = ''
            for char in string:
                if char == ',':
                    array.append(word)
                    word = ''
                else:
                    word = word + char
            array.append(word)
            return array
        else:
            return [string]
