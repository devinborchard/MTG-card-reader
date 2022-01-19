import json
import Sql
import shutil
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfile


class UpdateTab:
    def __init__(self, tab_control):
        self.frame = ttk.Frame(tab_control)
        self.cards_list = []

        self.file_path = ''
        self.data = ''

        self.file_label = tk.Label(
            self.frame,
            text='Upload AllPrintings JSON File'
        )
        self.file_label.grid(row=0, column=0, padx=10)

        self.file_upload_button = tk.Button(
            self.frame,
            text='Choose File',
            command=lambda: self.open_file()
        )
        self.file_upload_button.grid(row=0, column=1)

        self.upload_button = tk.Button(self.frame, text='Update', command=self.update)

        self.file_status_label = tk.Label(self.frame, text='Waiting...')
        self.file_status_label.grid(row=1, column=1)

        # set up the widgets

    def update(self):
        print('uploading')
        self.file_status_label.config(text='Updating...')
        progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL,
                                   length=100, mode='determinate')

        progress.grid(row=0, column=3, padx=6)
        progress['value'] = 0
        self.frame.update_idletasks()

        all_printings = json.loads(self.data)['data']

        set_keys = list(all_printings.keys())

        # get length
        total = 0
        for set_key in set_keys:
            set_ = all_printings[set_key]
            for card in set_['cards']:
                total = total+1
        print('count', total)
        # start querying

        connection = Sql.get_connection()

        table = 'mtg.all_printings'

        data = Sql.read_query(connection, 'SELECT * FROM ' + table + ';')
        names = []
        for element in data:
            names.append(element[1])

        # print(names)

        count = 0
        for set_key in set_keys:
            set_ = all_printings[set_key]

            for card in set_['cards']:

                count = count + 1
                progress_value = int(count/total*100)
                print(progress_value)
                if progress_value % 5:
                    progress['value'] = progress_value
                    self.frame.update_idletasks()

                while "\"" in card['name']:
                    card['name'] = card['name'].replace("\"", "#")

                if card['name'] not in names:
                    print(card['name'])
                    self.cards_list.append(card)
                    Sql.store_card(card, 'mtg.all_printings', connection)

        self.file_status_label.config(text='Done!')

    def open_file(self):
        self.file_path = askopenfile(mode='r', filetypes=[('JSON Files', '*json')])
        # print(self.file_path.name)
        if self.file_path is not None:
            try:
                with open('card_reader/AllPrintings.json', 'r', encoding="utf8") as myfile:
                    self.data = myfile.read()
                    self.file_status_label.config(text='File Uploaded!')
                    self.upload_button.grid(row=0, column=2, sticky=tk.W, pady=4)

            except:
                print('ERROR: Could not read file')
        else:
            print('ERROR: File not uploaded correctly')





