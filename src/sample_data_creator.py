
from typing import Dict, Any
import mysql.connector
import pandas as pd
from utils import get_final_path, read_json


class DataCreator:

    def __init__(self, table_name: str = 'bt') -> None:

        data_path: str = get_final_path(1, ['data', 'books.csv'])
        conf_path: str = get_final_path(1, ['conf.json'])
        self.df_: pd.DataFrame = pd.read_csv(data_path)
        self.conf: Dict[str, Any] = read_json(conf_path)
        self.table_name: str = table_name

    def to_mysql(self) -> None:

        # connecting to the database
        database = mysql.connector.connect(
            host = self.conf['HOST'],
            user = self.conf['USER'],
            passwd = self.conf['PASSWD'],
            database = self.conf['DATABASE']
        )
        cursor_object = database.cursor()
        # Checking if the table exist in db
        sql = 'SHOW TABLES'
        cursor_object.execute(sql)
        res = cursor_object.fetchall()
        if (self.table_name,) not in res:
            table_records = """CREATE TABLE {} (
                        ID INT AUTO_INCREMENT PRIMARY KEY,
                        Title VARCHAR(200),
                        Author VARCHAR(200),
                        Genre VARCHAR(200),
                        Height INT,
                        Publisher VARCHAR(200)
                        )""".format(self.table_name)
            cursor_object.execute(table_records)
            database.commit()
        else:
            pass
        for i in range(len(self.df_)):
            _title = str(self.df_['Title'][i])
            _author = str(self.df_['Author'][i])
            _genre = str(self.df_['Genre'][i])
            _height = str(self.df_['Height'][i])
            _publisher = str(self.df_['Publisher'][i])
            val = (_title, _author, _genre, _height, _publisher)
            sql = "INSERT INTO {} (Title, Author, Genre, Height, Publisher) VALUES (%s, %s, %s, %s, %s)".format(self.table_name)
            cursor_object.execute(sql, val)
            database.commit()
        database.close()

        return


if __name__ == '__main__':

    DataCreator().to_mysql()
