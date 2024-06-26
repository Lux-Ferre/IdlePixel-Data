import os
import dotenv

import mysql.connector

from datetime import datetime
from mysql.connector import errorcode

from models import TCGTableRow, CardName, PlayerName, PlayerItems

dotenv.load_dotenv()    # Handles env vars during development


class Repo:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("fastapi_mysql_host"),
                user=os.getenv("fastapi_mysql_user"),
                password=os.getenv("fastapi_mysql_password"),
                database="idlepixel"
            )

            return self
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def get_table(self, table: str) -> list:
        cursor = self.connection.cursor()

        query = "SELECT * FROM " + table
        params = tuple()

        cursor.execute(query, params)

        return cursor.fetchall()

    def get_cols_for_table(self, table: str) -> list:
        cursor = self.connection.cursor()

        query = "SHOW COLUMNS FROM " + table
        params = tuple()

        cursor.execute(query, params)

        return [column[0] for column in cursor.fetchall()]

    def query_full_column(self, table: str, col: str):
        cursor = self.connection.cursor()

        query = f"SELECT {col} FROM {table}"
        params = tuple()

        cursor.execute(query, params)

        return cursor.fetchall()

    def simple_query(self, table: str, col: str, param):
        cursor = self.connection.cursor()

        query = f"SELECT * FROM {table} WHERE {col}=%s"
        params = (param,)

        cursor.execute(query, params)

        return cursor.fetchall()

    def single_value_query(self, table: str, selection: str, where: str, param):
        cursor = self.connection.cursor()

        query = f"SELECT {selection} FROM {table} WHERE {where}=%s"
        params = (param,)

        cursor.execute(query, params)

        return cursor.fetchall()[0][0]

    # game_tcg
    def get_tcg_table(self) -> list:
        table_data = self.get_table("game_tcg")

        return table_data

    def cache_next_page(self, cache_page):
        cursor = self.connection.cursor()
        page_size = 200
        start_id = cache_page * page_size
        query = f"SELECT * FROM game_tcg WHERE id > {start_id} ORDER BY id LIMIT {page_size}"
        params = tuple()

        cursor.execute(query, params)

        return cursor.fetchall()

    def get_card_name_from_id(self, id_num: int) -> CardName | None:
        result = self.simple_query("game_tcg", "id", id_num)
        if result:
            return CardName(id=id_num, name=result[0][1])
        else:
            return None

    def get_owner_id_from_card_id(self, id_num: int) -> int | None:
        result = self.simple_query("game_tcg", "id", id_num)
        if result:
            return result[0][3]
        else:
            return None

    def get_collection_from_player_name(self, player_name: str):
        id_result = self.simple_query("player_id_name_view", "username", player_name)

        player_id = id_result[0][0]

        collection_result = self.simple_query("game_tcg", "player_id", player_id)

        return collection_result
    # end game_tcg

    # player_id_name_view
    def get_player_name_from_id(self, player_id: int) -> PlayerName | None:
        result = self.single_value_query("player_id_name_view", "username", "id", player_id)
        if result:
            return PlayerName(id=player_id, name=result)
        else:
            return None

    def get_id_from_player_name(self, player_name: str) -> PlayerName | None:
        result = self.simple_query("player_id_name_view", "username", player_name)
        if result:
            return PlayerName(id=result[0][0], name=player_name)
        else:
            return None
    # end player_id_name_view

    # player_view
    @staticmethod
    def parse_player_items(raw: str) -> dict[str, str]:
        data_array = raw.split("~")
        parsed_data = {}
        i = 0
        while i < len(data_array):
            parsed_data[data_array[i]] = data_array[i+1]
            i += 2

        return parsed_data

    def get_items_from_player_name(self, player_name: str) -> PlayerItems | None:
        result = self.single_value_query("player_view", "items", "username", player_name)
        if result:
            parsed_data = self.parse_player_items(result)
            return PlayerItems(items=parsed_data, name=player_name)
        else:
            return None

    def get_items_from_player_id(self, player_id: int) -> PlayerItems | None:
        result = self.single_value_query("player_view", "items", "id", player_id)
        if result:
            parsed_data = self.parse_player_items(result)
            return PlayerItems(items=parsed_data, id=player_id)
        else:
            return None

    def get_specific_items_from_player_name(self, player_name: str, req_items: list[str]) -> PlayerItems | None:
        result = self.single_value_query("player_view", "items", "username", player_name)
        if result:
            parsed_data = self.parse_player_items(result)
            fetched_items = {}
            for item in req_items:
                fetched_items[item] = parsed_data.get(item, None)
            return PlayerItems(items=fetched_items, name=player_name)
        else:
            return None

    def get_specific_items_from_player_id(self, player_id: int, req_items: list[str]) -> PlayerItems | None:
        result = self.single_value_query("player_view", "items", "id", player_id)
        if result:
            parsed_data = self.parse_player_items(result)
            fetched_items = {}
            for item in req_items:
                fetched_items[item] = parsed_data.get(item, None)
            return PlayerItems(items=fetched_items, id=player_id)
        else:
            return None
    # end player_view

    # hiscores_onelifehardcoredeaths
    def get_deaths_usernames(self) -> list[str]:
        result = self.query_full_column("hiscores_onelifehardcoredeaths", "username")
        if result:
            name_list = [n[0] for n in result]
            return name_list
        else:
            return []

    def get_levels_lost_per_enemy(self) -> dict[str, int]:
        cursor = self.connection.cursor()

        query = f"SELECT death_reason, SUM(global_level) FROM hiscores_onelifehardcoredeaths GROUP BY death_reason;"
        params = tuple()

        cursor.execute(query, params)

        result = cursor.fetchall()

        if result:
            return dict(result)
        else:
            return {}
