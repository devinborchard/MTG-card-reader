import tkinter as tk
from tkinter import ttk

from NewCardsTab import NewCardsTab
from Update import UpdateTab
from CollectionTab import CollectionTab


class Gui:

    def __init__(self):

        # whole app set up
        self.master = tk.Tk()
        self.master.title("MTG Card Collector")
        self.master.geometry('700x700')

        # set up the tabs
        tab_control = ttk.Notebook(self.master)

        self.new_cards_tab = NewCardsTab(tab_control)
        tab_control.add(self.new_cards_tab.frame, text='Add New Cards')

        self.update_tab = UpdateTab(tab_control)
        tab_control.add(self.update_tab.frame, text='Update')

        self.collection_tab = CollectionTab(tab_control)
        tab_control.add(self.collection_tab.frame, text='Collection')

        # run it
        tab_control.grid()
        tk.mainloop()


gui = Gui()
