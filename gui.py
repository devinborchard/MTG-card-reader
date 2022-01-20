import tkinter as tk
from tkinter import ttk

# import classes from other files to add the other tabs
from NewCardsTab import NewCardsTab
from Update import UpdateTab
from CollectionTab import CollectionTab


# Run this file to launch the application
class Gui:

    def __init__(self):

        # tkinter window setup
        self.master = tk.Tk()  # initialize tkinter root
        self.master.title("MTG Card Collector")  # rename the app window
        self.master.geometry('700x700')  # set the window size to 700 x 700

        # create new tabs from class objects and add them to the window
        tab_control = ttk.Notebook(self.master)  # create the object to add tabs to the window

        self.new_cards_tab = NewCardsTab(tab_control)
        tab_control.add(self.new_cards_tab.frame, text='Add New Cards')

        self.update_tab = UpdateTab(tab_control)
        tab_control.add(self.update_tab.frame, text='Update')

        self.collection_tab = CollectionTab(tab_control)
        tab_control.add(self.collection_tab.frame, text='Collection')

        # run it
        tab_control.grid()  # add the tabs to the window
        tk.mainloop()


gui = Gui()  # initialize the class
