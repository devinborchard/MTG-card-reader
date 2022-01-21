# MTG-card-reader
The purpose of the application is to provide Magic the Gathering players with
a way to sort through their collection of cards when building a deck, or
looking for specific cards that have different properties. It can be difficult
to do this by hand when most people have their physical cards all piled in
a box somewhere with little to no organization.

Using the app a user can import pictures that they have taken of the cards
in their collection, and the app will extract the title of the card using
python image libraries. It will then use the card's title to find the card
in a database containing all the cards ever printed. Once the card's data is
found it is stored in a different database containing all cards in
the user's collection. The user can then use the app to sort through this
collection database to find specific cards they are looking for.

The databases are run on a local SQL server. Two tables are needed, one for
all the card printings, and one for the user's collection. To fill out the
table containing all printings the user will need the latest AllPrintings.JSON
file from https://mtgjson.com/downloads/all-files/#allprintings. This website
contains a download link for a file in JSON format containing all the data.
The user can drop that file into a file import widget on the Update tab of the
app to fill in the table. Whenever a new Magic card set is released and a new
AllPrintings.JSON is updated online. The user can download the new file and
update the application when needed.


# Imporovements
At the moment the functionality for reading in cards from images is
finicky. The images have to be perfectly aligned to work. I am working to
write code that will detect the edges of the card in the image and will rotate
and cut the image so that pictures can be taken more freely.

In Magic the Gathering many cards are reprinted from set to set that gets
released. This means that the same card could belong to different sets. This is
important when you get into different game modes of Magic where you can only use
cards from specific sets. At the moment when a card is read the set is not read
in with it, just the card data. Functionality needs to be added to somehow
determine the set of the card based on the image.
