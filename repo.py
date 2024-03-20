import os
import dotenv

import mysql.connector

from datetime import datetime
from mysql.connector import errorcode

from models import TCGTableRow, CardName

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

    def simple_query(self, table: str, col: str, param):
        cursor = self.connection.cursor()

        query = f"SELECT * FROM {table} WHERE {col}=%s"
        params = (param,)

        cursor.execute(query, params)

        return cursor.fetchall()

    def get_tcg_table(self) -> list[TCGTableRow]:
        table_data = self.get_table("game_tcg")

        parsed_data = []

        for row in table_data:
            parsed_data.append(
                TCGTableRow(
                    id=row[0],
                    name=row[1],
                    holo=bool(row[2]),
                    player_id=row[3],
                    datetime=row[4],
                )
            )

        return parsed_data

    def get_card_name_from_id(self, id_num: int) -> CardName | None:
        result = self.simple_query("game_tcg", "id", id_num)
        if result:
            return CardName(id=id_num, name=result[0][1])
        else:
            return None