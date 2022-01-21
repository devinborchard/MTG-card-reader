import json
import Sql
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfile


# class to create the update tab of the application to update the All printings database
class UpdateTab:
    def __init__(self, tab_control):  # needs the tab control to add tab to window
        self.frame = ttk.Frame(tab_control)  # create a frame for the widgets

        # create variables for later and give default values
        self.file_path = ''
        self.data = ''

        # create widgets
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

        # create label for updating the user on whats processing
        self.file_status_label = tk.Label(self.frame, text='Waiting...')
        self.file_status_label.grid(row=1, column=1)

    # asdf
    def update(self):
        print('uploading')

        # update the status widget
        self.file_status_label.config(text='Updating...')

        # create a progress bar to show status of the update
        progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL,
                                   length=100, mode='determinate')
        progress.grid(row=0, column=3, padx=6)
        progress['value'] = 0

        self.frame.update_idletasks()  # update the progress bar

        all_printings = json.loads(self.data)['data']  # get the JSON data from the file data
        set_keys = list(all_printings.keys())  # data is keyed by sets so get the keys

        # get length
        total = 0
        for set_key in set_keys:
            set_ = all_printings[set_key]
            for card in set_['cards']:
                total = total+1

        # start querying
        connection = Sql.get_connection()

        table = 'mtg.all_printings'  # table containing the data for all printings

        # get the names of all the cards that are currently stored in the database
        data = Sql.read_query(connection, 'SELECT * FROM ' + table + ';')
        names = []
        for element in data:
            names.append(element[1])

        # store new cards
        count = 0
        for set_key in set_keys:
            set_ = all_printings[set_key]

            for card in set_['cards']:

                count = count + 1

                # update progress bar if multiple of 5
                progress_value = int(count/total*100)
                print(progress_value)
                if progress_value % 5:
                    progress['value'] = progress_value
                    self.frame.update_idletasks()

                # replace all " chars in card names with a # so they don't interfere with SQL queries
                while "\"" in card['name']:
                    card['name'] = card['name'].replace("\"", "#")

                # if the current card read from the JSON data is not already in the database then add it
                if card['name'] not in names:
                    print(card['name'])
                    Sql.store_card(card, 'mtg.all_printings', connection)

        # once finished update the status label to tell the user
        self.file_status_label.config(text='Done!')

    # function to read in the JSON file and extract the data
    def open_file(self):
        self.file_path = askopenfile(mode='r', filetypes=[('JSON Files', '*json')])  # prompt user for the JSON file

        if self.file_path is not None:
            try:
                with open('card_reader/AllPrintings.json', 'r', encoding="utf8") as myfile:
                    self.data = myfile.read()
                    self.file_status_label.config(text='File Uploaded!')

                    # give the user the update button once the file is read in
                    self.upload_button.grid(row=0, column=2, sticky=tk.W, pady=4)
            except:
                print('ERROR: Could not read file')
        else:
            print('ERROR: File not uploaded correctly')
