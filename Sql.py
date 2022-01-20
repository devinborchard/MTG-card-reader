import mysql.connector
from mysql.connector import Error

# this file contains function to interact with the SQL database that holds the card data


# function to create a connection the SQL server to be passed to other function
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


# function to create a connection to a specific SQL database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


# function to execute a write query to the database
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# function to execute a read query and return the data
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


# create a database connection with the username and password for the MTG card databases
def get_connection():
    connection = create_db_connection("localhost", "root", 'password', "mtg")
    return connection


# function to score a card data object in the card database
def store_card(card, table, quantity, connection):
    print(card)

    # replace the \ characters in strings with # so they can be included in SQL queries
    while "\"" in card[2]:
        card[2] = card[2].replace("\"", "#")

    while "\"" in card[1]:
        card[1] = card[1].replace("\"", "#")

    while "\"" in card[12]:
        card[12] = card[12].replace("\"", "#")

    # construct the query string with all of the data values from the card object
    values_string = ' values ({},"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",' \
                    '"{}","{}","{}","{}","{}","{}","{}",{});'.format(get_number_of_cards(table, connection) + 1,
                                                                     card[1], card[2], card[3], card[4], card[5],
                                                                     card[6], card[7], card[8], card[9], card[10],
                                                                     card[11], card[12], card[13], card[14], card[15],
                                                                     card[16], card[17], card[18], quantity)

    execute_query(connection, 'INSERT INTO ' + table + values_string)


# returns the number of card objects stored in a database
def get_number_of_cards(table, connection):
    result = read_query(connection, 'SELECT * FROM '+table+';')
    return len(result)

