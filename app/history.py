# coding=utf-8

import pymysql as ps
import pymysql.cursors


def connection():
    return ps.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='chatbot',
        cursorclass=pymysql.cursors.DictCursor
    )


def oper1():
    connection = ps.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='chatbot',
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            connection.ping(reconnect=True)
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


def oper():
    conn = connection()
    with conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO `chatbot_history` (`user_id`, `type`, `message`) VALUES (%s, %s, %s)"
            cursor.execute(sql, ("1234546", 0, "Hello"))
    conn.commit()


if __name__ == "__main__":
    oper()
