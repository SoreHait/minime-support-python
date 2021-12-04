import sqlite3
import random
from Util.exceptions import *

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
modifiable_items = [8000, 110, 5060, 5230, 5310, 5410]

class SqlQuery():
    def __init__(self, dbPath):
        self.dbPath = dbPath

    def get_id_by_aime(self, aime):
        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        cur.execute("SELECT id FROM cm_user_data WHERE access_code = ?", (aime,))
        id_list = cur.fetchall()
        if len(id_list) == 0:
            raise UserNotFoundException
        return id_list[0][0]

    def query_data(self, felica, tableName):
        if felica == '' or felica == None:
            raise CardNoEntryException
        if tableName == '' or tableName == None:
            raise TableNameNoEntryException
        if tableName not in all_table:
            raise TableNotAvailableException
        try:
            aime = felica2aime(felica)
        except ValueError:
            raise CardInvalidException
        id = self.get_id_by_aime(aime)

        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        if tableName in table_using_id:
            cur.execute(f"SELECT * FROM {tableName} WHERE id = ?", (id,))
        else:
            cur.execute(f"SELECT * FROM {tableName} WHERE profile_id = ?", (id,))
        column_name = [str(name[0]) for name in cur.description]
        data_raw = cur.fetchall()
        if len(data_raw) == 0:
            return []
        return [dict(zip(column_name, [str(item) for item in data_element])) for data_element in data_raw]

    def item_operation(self, felica, action, item_id, item_count):
        if felica == '' or felica == None:
            raise CardNoEntryException
        try:
            aime = felica2aime(felica)
        except ValueError:
            raise CardInvalidException
        id = self.get_id_by_aime(aime)

        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        if action == 'modify':
            if (item_id == '' or item_id == None) or (item_count == '' or item_count == None):
                raise ParamInsufficientException
            if int(item_id) not in modifiable_items:
                raise ItemIdInvalidException

            cur.execute("SELECT * FROM cm_user_item WHERE profile_id = ? AND item_id = ? AND item_kind = 5", (id, item_id))
            item = cur.fetchall()
            if len(item) == 0:
                # insert item if item not exist
                cur.execute("INSERT INTO cm_user_item (id, profile_id, item_kind, item_id, stock, is_valid) VALUES (?,?,?,?,?,?)", (generate_id(), id, 5, item_id, item_count, 'true'))
                conn.commit()
            else:
                # modify count if item exists
                cur.execute("UPDATE cm_user_item SET stock = ? WHERE profile_id = ? AND item_kind = 5 AND item_id = ?", (item_count, id, item_id))
                conn.commit()
            return {'code': 0, 'msg': 'success'}

        elif action == 'fetch':
            item_list = " OR ".join([f"item_id = {i}" for i in modifiable_items])
            cur.execute(f"SELECT * FROM cm_user_item WHERE profile_id = ? AND ({item_list}) AND item_kind = 5", (id,))
            column_name = [str(name[0]) for name in cur.description]
            data_raw = cur.fetchall()
            if len(data_raw) == 0:
                return []
            return [dict(zip(column_name, [str(item) for item in data_element])) for data_element in data_raw]
        else:
            raise ActionInvalidException

    def mod_user_info(self, felica, user_name, team_name):
        if felica == '' or felica == None:
            raise CardNoEntryException
        if (user_name == '' or user_name == None) and (team_name == '' or team_name == None):
            raise ModifyInfoNotFoundException
        try:
            aime = felica2aime(felica)
        except ValueError:
            raise CardInvalidException
        id = self.get_id_by_aime(aime)

        conn = sqlite3.connect(self.dbPath)
        cur = conn.cursor()
        if user_name != None and len(user_name) > 0:
            try:
                cur.execute("UPDATE cm_user_data SET user_name = ? WHERE access_code = ?", (user_name, aime))
                conn.commit()
            except Exception:
                raise ModifyFailure

        if team_name != None and len(team_name) > 0:
            try:
                cur.execute("SELECT * FROM cm_user_general_data WHERE profile_id = ? AND key = 'user_team_name'", (id,))
                name = cur.fetchall()
                if len(name) == 0:
                    cur.execute("INSERT INTO cm_user_general_data (id, profile_id, key, value) VALUES (?,?,?,?)", (generate_id(), id, 'user_team_name', team_name))
                    conn.commit()
                else:
                    cur.execute("UPDATE cm_user_general_data SET value = ? WHERE profile_id = ? AND key = ?", (team_name, id, 'user_team_name'))
                    conn.commit()
            except Exception:
                raise ModifyFailure

        return {'code': 0, 'msg': 'success'}

def generate_id():
    return str(random.randint(0, 0xFFFFFFFFFFFFFFFF))

def felica2aime(felica):
    return str(int(felica, 16)).rjust(20, '0')
