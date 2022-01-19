import tkinter as tk
import json
import pathlib
from card_reader import cardReader
import Sql
from tkinter import ttk
import PIL
from PIL import Image


def get_config():
    with open('config.txt') as f:

        configurations = {}
        line = f.readlines()
        string_config = line[0]

        config = json.loads(string_config)

        return config


def save_config(config):
    s = json.dumps(config)
    print(s)
    with open('config.txt', 'w') as f:
        f.write(s)


# whole app set up
master = tk.Tk()
master.title("MTG Card Collector")
master.geometry('500x500')

tab_control = ttk.Notebook(master)

home_tab = ttk.Frame(tab_control)
tab_control.add(home_tab, text='Home')

new_cards_tab = ttk.Frame(tab_control)
tab_control.add(new_cards_tab, text='Add New Cards')

collection_tab = ttk.Frame(tab_control)
tab_control.add(collection_tab, text='Collection')


########################### Home tab
###########################

########################### Add new Cards tab
###########################
def get_number_of_new_cards():

    initial_count = 0
    for path in pathlib.Path(e1.get()).iterdir():
        if path.is_file():
            initial_count += 1
    return initial_count


def save_new_image_path():
    config = get_config()
    path = e1.get()
    config["new_image_path"] = path
    save_config(config)
    textBox_number_of_new_cards.config(text="Currently {} Cards in directory".format(get_number_of_new_cards()))


def read_cards_in_path():
    cards = cardReader.run(e1.get())
    global cards_list
    cards_list = cards
    print(cards)
    for i, card in enumerate(cards):
        listbox.insert(i, card['data']['name'])


def list_items_selected(event):
    global cards_list
    # get selected indices
    selected_indices = listbox.curselection()

    img = Image.open(cards_list[selected_indices[0]]['path'])
    img_resized = img.resize((265, 370))
    img = PIL.ImageTk.PhotoImage(img_resized)
    image_label = tk.Label(new_cards_tab, image=img)
    image_label.image = img
    image_label.grid(row=3, column=1, sticky=tk.W, pady=4)




cards_list = []
config = get_config()
tk.Label(new_cards_tab, text="New Cards Images Paths").grid(row=0)
e1 = tk.Entry(new_cards_tab, width=50)
e1.insert(0, config["new_image_path"])

e1.grid(row=0, column=1)


tk.Button(new_cards_tab, text='Save Path', command=save_new_image_path).grid(row=1, column=1, sticky=tk.W, pady=4)
tk.Button(new_cards_tab, text='Read Cards', command=read_cards_in_path).grid(row=2, column=0, sticky=tk.W, pady=4)

number_of_new_cards = get_number_of_new_cards()
print(number_of_new_cards)

# Create label
textBox_number_of_new_cards = tk.Label(new_cards_tab,
                                       text="Currently {} Cards in directory".format(number_of_new_cards))
textBox_number_of_new_cards.grid(row=2, column=1)

listbox = tk.Listbox(new_cards_tab)
listbox.grid(row=3, column=0, sticky=tk.W, pady=4)
listbox.bind('<<ListboxSelect>>', list_items_selected)



########################### Collection Tab
###########################
def populate_collection_list(query):
    connection = Sql.get_connection()
    result = Sql.read_query(connection, query)
    for item in result:
        collection_list.insert(tk.END, item[1])


my_scroll = tk.Scrollbar(collection_tab)
my_scroll.pack(side=tk.RIGHT, fill=tk.Y)

collection_list = tk.Listbox(collection_tab, yscrollcommand=my_scroll.set)
populate_collection_list('SELECT * FROM mtg.cards;')
collection_list.pack(side=tk.LEFT, fill=tk.BOTH)

my_scroll.config(command=collection_list.yview)


########################## running it
tab_control.pack(expand=1, fill='both')
tk.mainloop()
