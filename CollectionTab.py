import tkinter as tk
import pathlib
from card_reader import cardReader
from tkinter import ttk
from PIL import ImageTk
import PIL
import Sql
import cv2


class CollectionTab:
    def __init__(self, tab_control):
        self.frame = ttk.Frame(tab_control)
        self.cards_list = []
        self.get_owned_cards()
        self.current_shown_cards = self.cards_list
        self.deck_list = []

        tk.Label(self.frame, text=" ").grid(row=0, column=0)

        # top row where different lookup parameters are made available
        row1_frame = tk.Frame(self.frame)
        row1_frame.grid(row=0, column=0)

        row2_frame = tk.Frame(self.frame)
        row2_frame.grid(row=1, column=0)

        row3_frame = tk.Frame(self.frame)
        row3_frame.grid(row=2, column=0)

        row4_frame = tk.Frame(self.frame)
        row4_frame.grid(row=3, column=0)

        # entry for the search by name

        tk.Label(row1_frame, text="Card Name:").grid(row=0, column=0)
        self.entry_card_name = tk.Entry(row1_frame, width=30)
        self.entry_card_name.grid(row=0, column=1)

        # entry for searching by color
        tk.Label(row1_frame, text="Colors:").grid(row=0, column=2)

        self.w_check = tk.IntVar()
        self.b_check = tk.IntVar()
        self.bl_check = tk.IntVar()
        self.r_check = tk.IntVar()
        self.g_check = tk.IntVar()

        self.w_check_box = tk.Checkbutton(row1_frame, variable=self.w_check, background='#EBE8C2').grid(row=0, column=3)
        self.b_check_box = tk.Checkbutton(row1_frame, variable=self.b_check, background='#2C20DC').grid(row=0, column=4)
        self.bl_check_box = tk.Checkbutton(row1_frame, variable=self.bl_check, background='black').grid(row=0, column=5)
        self.r_check_box = tk.Checkbutton(row1_frame, variable=self.r_check, background='#DC2026').grid(row=0, column=6)
        self.g_check_box = tk.Checkbutton(row1_frame, variable=self.g_check, background='#287D30').grid(row=0, column=7)

        # entry for searching by mana cost
        tk.Label(row1_frame, text="Mana Cost:").grid(row=0, column=8)
        self.entry_mana_cost = tk.Entry(row1_frame, width=2)
        self.entry_mana_cost.grid(row=0, column=9)

        # clear search Button
        tk.Button(row2_frame, text='Clear All', command=self.search_clear).grid(row=0, column=0, sticky=tk.W, pady=4)

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

        # searching List box
        self.search_list_box = tk.Listbox(row3_frame)
        self.search_list_box.grid(row=0, column=0, sticky=tk.W, pady=4)
        self.search_list_box.bind('<<ListboxSelect>>', self.select_list_item)

        self.image_label = tk.Label(row3_frame)
        self.image_label.grid(row=0, column=1, sticky=tk.W, pady=4)

        self.deck_list_box = tk.Listbox(row3_frame)
        self.deck_list_box.grid(row=0, column=2, sticky=tk.W, pady=4)
        self.deck_list_box.bind('<<ListboxSelect>>', self.select_list_item)
        self.update_list_box()



        # add widgets for creating a deck
        deck_info_frame = tk.Frame(row3_frame)
        deck_info_frame.grid(row=0, column=3)

        tk.Label(deck_info_frame, text="Deck Name:").grid(row=0, column=0)

        self.entry_deck_name = tk.Entry(deck_info_frame, width=10)
        self.entry_deck_name.grid(row=1, column=0)

        tk.Button(deck_info_frame, text='Save Deck', command=self.save_deck).grid(row=2, column=0, sticky=tk.W, pady=4)

        tk.Button(row4_frame, text='Add', command=self.add_card).grid(row=0, column=0, sticky=tk.W, pady=4)

    def save_deck(self):
        # deck = self.entry_deck_name.get()
        # print('SAVing ', deck)
        with open('decks/'+self.entry_deck_name.get()+'.txt', 'w') as f:
            text = ''
            for card in self.deck_list:
                text = text+card['card'][1]+'|'
            f.write(text)

    def add_card(self):
        if self.search_list_box.curselection():
            # print('NOT EMPTY')
            selected_indices = self.search_list_box.curselection()[0]
            self.deck_list.append(self.current_shown_cards.pop(selected_indices))
            self.update_list_box()

    def update_card_image(self):
        img = []
        if self.search_list_box.curselection():
            selected_indices = self.search_list_box.curselection()[0]
            img = self.current_shown_cards[selected_indices]["img"]

        elif self.deck_list_box.curselection():
            selected_indices = self.deck_list_box.curselection()[0]
            img = self.deck_list[selected_indices]["img"]

        self.image_label.config(image=img)
        self.image_label.image = img

    def search_cards(self):
        print('searching')
        name = self.entry_card_name.get()
        mana_cost = self.entry_mana_cost.get()
        types = self.entry_card_type.get()
        keywords = self.entry_key_words.get()

        # get multiple values from entries that can get mulitple values
        types = self.string_to_array(types)
        keywords = self.string_to_array(keywords)

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
        # print(conditions)

        condition_str = ''
        if len(conditions) == 1:
            condition_str = conditions[0]
        elif len(conditions) > 1:
            for i in range(len(conditions)-1):
                condition_str = condition_str + conditions[i] + ' AND '
            condition_str = condition_str + conditions[len(conditions)-1]
        else:
            self.current_shown_cards = self.cards_list
            self.update_list_box()
            self.update_card_image()
            return
        # print(condition_str)
        connection = Sql.get_connection()
        query = 'SELECT * FROM mtg.cards WHERE '+condition_str+';'
        # print(query)
        found_cards = Sql.read_query(connection, query)
        self.current_shown_cards = []
        for card in found_cards:
            # print('card: ',card)
            img = []
            for loaded_card in self.cards_list:
                # print('LOADED: ',loaded_card)
                # print("loaded: ",loaded_card)

                if loaded_card["card"][1] == card[1]:
                    img = loaded_card["img"]
            self.current_shown_cards.append({"card": card, "img": img})
        # print('done: ',self.current_shown_cards)
        self.update_list_box()

    def search_clear(self):
        print('CLEAR')

    def update_list_box(self):
        self.search_list_box.delete(0, tk.END)
        self.deck_list_box.delete(0, tk.END)
        # print('SHOWING: ', self.current_shown_cards)
        for i, card in enumerate(self.current_shown_cards):
            # print(card)
            self.search_list_box.insert(i, card["card"][1])

        for i, card in enumerate(self.deck_list):
            self.deck_list_box.insert(i, card["card"][1])

    def select_list_item(self, event):
        self.update_card_image()

    def get_owned_cards(self):
        connection = Sql.get_connection()
        # all_cards = Sql.read_query(connection, 'Select * from mtg.all_printings;')
        owned_cards = Sql.read_query(connection, 'Select * from mtg.cards;')

        for card in owned_cards:
            card_data = Sql.read_query(connection, 'Select * from mtg.all_printings where name = "'+card[1]+'";')
            name = card_data[0][1]
            img = PIL.Image.open('card_reader/imgs/' + name + '.png')
            img_resized = img.resize((265, 370))
            img = ImageTk.PhotoImage(img_resized)

            self.cards_list.append({"card": card_data[0], "img": img})

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
