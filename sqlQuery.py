import sqlite3
from exceptions import *

all_table = [
    'cm_user_activity',
    'cm_user_character',
    'cm_user_course',
    'cm_user_duel_list',
    'cm_user_item',
    'cm_user_map',
    'cm_user_music',
    'cm_user_playlog',
    'cm_user_general_data',
    'cm_user_data',
    'cm_user_data_ex',
    'cm_user_game_option',
    'cm_user_game_option_ex'
]
table_using_id = [
    'cm_user_data',
    'cm_user_data_ex',
    'cm_user_game_option',
    'cm_user_game_option_ex'
]

class SqlQuery():
    def __init__(self, dbPath):
        self.conn = sqlite3.connect(dbPath, check_same_thread = False)
        self.cursor = self.conn.cursor()

    def query_data(self, felica, tableName):
        if tableName == '':
            raise TableNameNoEntryException
        if tableName not in all_table:
            raise TableNotAvailableException
        if felica == '':
            raise CardNoEntryException
        aime = str(int(felica, 16)).rjust(20, '0')
        self.cursor.execute(f"SELECT id FROM cm_user_data WHERE access_code = '{aime}'")
        id_list = self.cursor.fetchall()
        if len(id_list) == 0:
            raise UserNotFoundException
        id = id_list[0][0]
        if tableName in table_using_id:
            self.cursor.execute(f"SELECT * FROM {tableName} WHERE id = '{id}'")
        else:
            self.cursor.execute(f"SELECT * FROM {tableName} WHERE profile_id = {id}")
        column_name = [str(name[0]) for name in self.cursor.description]
        data_raw = self.cursor.fetchall()
        data = [dict(zip(column_name, [str(item) for item in data_element])) for data_element in data_raw]
        return data
