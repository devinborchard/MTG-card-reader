import mysql.connector
from mysql.connector import Error
import pandas as pd


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


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def get_connection():
    connection = create_db_connection("localhost", "root", 'password', "mtg")
    return connection


def store_card(card, table, quantity, connection):
    print(card)

    while "\"" in card[2]:
        card[2] = card[2].replace("\"", "#")

    while "\"" in card[1]:
        card[1] = card[1].replace("\"", "#")

    while "\"" in card[12]:
        card[12] = card[12].replace("\"", "#")

    values_string = ' values ({},"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",{});'.format(
        get_number_of_cards(table, connection) + 1, card[1], card[2], card[3], card[4], card[5], card[6], card[7], card[8], card[9], card[10], card[11], card[12], card[13], card[14], card[15], card[16], card[17], card[18], quantity)


    execute_query(connection, 'INSERT INTO ' + table + values_string)


    '''keys = card.keys()
    if 'flavorText' not in keys:
        card['flavorText'] = "NULL"
    if 'text' not in keys:
        card['text'] = "NULL"
    if 'power' not in keys:
        card['power'] = "NULL"
    if 'toughness' not in keys:
        card['toughness'] = "NULL"
    if 'manaCost' not in keys:
        card['manaCost'] = "0"


    while "\"" in card['text']:
        card['text'] = card['text'].replace("\"", "#")

    while "\"" in card['name']:
        card['name'] = card['name'].replace("\"", "#")

    while "\"" in card['flavorText']:
        card['flavorText'] = card['flavorText'].replace("\"", "#")

    execute_query(connection, 'INSERT INTO '+table+' values '
                              '({},"{}","{}","{}","{}","{}","{}","{}","{}","{}",'
                              '"{}","{}","{}","{}","{}","{}","{}","{}","{}");'.format(
                                get_number_of_cards(table, connection)+1, card['name'], card['text'], card['colors'],
                                card['manaCost'], card['convertedManaCost'], card['colorIdentity'], card['identifiers'], card['number'],
                                card['power'], card['toughness'], card['types'], card['flavorText'], card['legalities'],
                                card['printings'], card['rarity'], card['setCode'], card['subtypes'], card['supertypes'],)
                  )
    '''

def get_number_of_cards(table, connection):
    result = read_query(connection, 'SELECT * FROM '+table+';')
    return len(result)


# execute_query(connection, 'INSERT INTO mtg.cards values (2,"test2","testtext2");')
# result = read_query(connection, 'SELECT * FROM mtg.cards;')
# print(result)

