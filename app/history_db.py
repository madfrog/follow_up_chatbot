# coding=utf-8

import mysql.connector
from mysql.connector import Error
from typing import List
from tools.singleton import Singleton


@Singleton
class HistoryHandler(object):
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='xxxxx',
            port=3306,
            user='root',
            password='xxxx',
            database='flask_demo',
        )
        if self.connection.is_connected():
            db_info = self.connection.get_server_info()
            print(f'db info: {db_info}')
        else:
            raise Exception("Get db connection failed")

    def insert_one_history(self, **history):
        cur = self.connection.cursor()
        sql = "INSERT INTO `chatbot_history` (`user_id`, `session_id`, `type`, `message`) VALUES (%s, %s, %s, %s);"
        cur.execute(sql, (history['user_id'], history['session_id'],
                    history['type'], history['message']))
        self.connection.commit()

    def fetch_latest_history(self, user_id):
        with self.connection.cursor() as cur:
            sql = 'SELECT * FROM `chatbot_history` WHERE `user_id`=%s ORDER BY `gmt_create` DESC LIMIT 1;'
            params = (user_id,)
            cur.execute(sql, params)
            records = cur.fetchall()
            if len(records) > 0:
                return records[0]
            else:
                print(f'Not get any one message for {user_id}')
                return []

    def fetch_all_history(self, user_id, session_id) -> List:
        with self.connection.cursor() as cur:
            sql = "SELECT * FROM `chatbot_history` WHERE  user_id=%s AND session_id=%s order by `gmt_create` ASC;"
            cur.execute(sql, (user_id, session_id,))
            return cur.fetchall()


if __name__ == "__main__":
    handle = HistoryHandle()
    handle.init()

    new_history = {"user_id": "123", "session_id": "32cvdsxcx",
                   "type": 1, "message": "hello, I'm chatbot"}
    handle.insert_one_history(**new_history)
    new_history = {"user_id": "123", "session_id": "32cvdsxcx",
                   "type": 1, "message": "hello, I'm chatbot"}
    handle.insert_one_history(**new_history)

    user_id = "123"
    record = handle.fetch_latest_history(user_id)
    print(f'{record}')

    session_id = "32cvdsxcx"
    records = handle.fetch_all_history(user_id, session_id)
    for rc in records:
        print(f'{rc}\n')
