
from typing import Dict, Any, Tuple, Union
import mysql.connector
from utils import get_final_path, read_json


class SqlConnector:

    def __init__(self, query: str) -> None:

        self.query = query
        conf_path: str = get_final_path(1, ['conf.json'])
        self.conf: Dict[str, Any] = read_json(conf_path)

    def sql_connection(self) -> Tuple[Union[mysql.connector.cursor.MySQLCursor, Any], Any]:

        # connecting to the database
        database = mysql.connector.connect(
            host = self.conf['HOST'],
            user = self.conf['USER'],
            passwd = self.conf['PASSWD'],
            database = self.conf['DATABASE']
        )
        cursor_object = database.cursor()

        return cursor_object, database

    def sql_query_process(self, cursor_object: mysql.connector.cursor.MySQLCursor) -> object:

        cursor_object.execute(self.query)
        res = cursor_object.fetchall()

        return res

    def main(self) -> object:

        cursor_object, database = self.sql_connection()
        result = self.sql_query_process(cursor_object)
        database.close()

        return result


if __name__ == '__main__':

    QUERY = 'SELECT * FROM bt'
    res_ = SqlConnector(query = QUERY).main()
    print(res_)
