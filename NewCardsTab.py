import tkinter as tk
import pathlib
from card_reader import cardReader
from tkinter import ttk
from PIL import ImageTk
from Helpers import get_config, save_config
import Sql


class NewCardsTab:

    def __init__(self, tab_control):
        self.frame = ttk.Frame(tab_control)
        self.cards_list = []

        # set up the widgets
        self.config = get_config() # load in the app configurations
        tk.Label(self.frame, text="New Cards Images Paths").grid(row=0)
        self.entry_folder_path = tk.Entry(self.frame, width=50)
        self.entry_folder_path.insert(0, self.config["new_image_path"]) # set the default value to the saved path
        self.entry_folder_path.grid(row=0, column=1)

        tk.Button(self.frame, text='Save Path', command=self.save_new_image_path).grid(row=1, column=1, sticky=tk.W,
                                                                                       pady=4)
        tk.Button(self.frame, text='Read Cards', command=self.read_cards_in_path).grid(row=2, column=0, sticky=tk.W,
                                                                                       pady=4)

        number_of_new_cards = self.get_number_of_new_cards()
        print(number_of_new_cards)

        # Create label
        self.textBox_number_of_new_cards = tk.Label(self.frame,
                                               text="Currently {} Cards in directory".format(number_of_new_cards))
        self.textBox_number_of_new_cards.grid(row=2, column=1)

        self.listbox = tk.Listbox(self.frame)
        self.listbox.grid(row=3, column=0, sticky=tk.W, pady=4)
        self.listbox.bind('<<ListboxSelect>>', self.select_list_item)

        self.image_label = tk.Label(self.frame)
        self.image_label.grid(row=3, column=1, sticky=tk.W, pady=4)

        self.quantities = []
        self.label_quantity = tk.Label(self.frame, width=5)
        self.label_quantity.grid(row=4, column=1)
        tk.Button(self.frame, text='add', command=self.add_quantity).grid(row=5, column=1, sticky=tk.W, pady=4)
        tk.Button(self.frame, text='remove', command=self.remove_quantity).grid(row=6, column=1, sticky=tk.W, pady=4)
        tk.Button(self.frame, text='Store Cards', command=self.store_cards).grid(row=4, column=0, sticky=tk.W, pady=4)

    def store_cards(self):
        connection = Sql.get_connection()
        print(self.cards_list)
        for card in self.cards_list:
            card_data = Sql.read_query(connection, 'SELECT * FROM mtg.all_printings WHERE name = "'+card['name']+'";')
            Sql.store_card(card_data[0], 'mtg.cards', 1, connection)

    def add_quantity(self):
        selected_indices = self.listbox.curselection()[0]
        cur = self.quantities[selected_indices]+1
        self.quantities[selected_indices] = cur
        self.label_quantity.config(text=str(cur))

    def remove_quantity(self):
        selected_indices = self.listbox.curselection()[0]
        cur = self.quantities[selected_indices]-1
        if cur == 0:
            self.remove_card()
        else:
            self.quantities[selected_indices] = cur
            self.label_quantity.config(text=str(cur))

    def save_new_image_path(self):
        path = self.entry_folder_path.get()
        self.config["new_image_path"] = path
        save_config(self.config)
        self.textBox_number_of_new_cards.config(
            text="Currently {} Cards in directory".format(self.get_number_of_new_cards())
        )

    def remove_card(self):
        selected_indices = self.listbox.curselection()[0]
        self.cards_list.pop(selected_indices)
        self.listbox.delete(selected_indices)
        self.quantities.pop(selected_indices)

        if selected_indices > 0:
            self.listbox.selection_set(selected_indices-1)
        else:
            self.listbox.selection_set(len(self.cards_list) - 1)
        self.update_card_image()

    def read_cards_in_path(self):
        self.cards_list = cardReader.run(self.entry_folder_path.get())
        for i, card in enumerate(self.cards_list):
            self.listbox.insert(i, card['name'])
            self.quantities.append(1)

        self.listbox.selection_set(0)
        self.update_card_image()

        tk.Button(self.frame, text='Remove Card', command=self.remove_card).grid(row=3, column=2, sticky=tk.W,
                                                                                      pady=4)

    def get_number_of_new_cards(self):
        initial_count = 0
        for path in pathlib.Path(self.entry_folder_path.get()).iterdir():
            if path.is_file():
                initial_count += 1
        return initial_count

    def update_card_image(self):
        if self.listbox.curselection():
            # print('NOT EMPTY')
            selected_indices = self.listbox.curselection()[0]

            img = self.cards_list[selected_indices]["img"]
            img = ImageTk.PhotoImage(img)

            self.image_label.config(image=img)
            self.image_label.image = img

            self.label_quantity.config(text=str(self.quantities[selected_indices]))

        else:
            # print('EMPTY')
            img = []
            self.image_label.config(image=img)
            self.image_label.image = img

    def select_list_item(self, event):
        # print("print Trigger")
        self.update_card_image()
