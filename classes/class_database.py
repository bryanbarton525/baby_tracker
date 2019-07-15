import mysql.connector
import json
from datetime import datetime


class DataBase:
    """
    Class to manage different database connections and queries.
    """

    def __init__(self):
        with open('/home/tracker/configs/db_conn.json') as conf_file:
            data = json.load(conf_file)
            print(data)
        try:
            self.conn = mysql.connector.connect(**data['database_creds'])

        except mysql.connector.Error as error:
            print(error)

    def db_curs(self, query, data=None, insert_data=None):
        curs = self.conn.cursor(dictionary=True)

        if insert_data is None:

            try:
                curs.execute(query, data)
                results = curs.fetchall()
                curs.close()
            except mysql.connector.Error as error:
                print(error)
                results = error

            return results

        else:
            try:
                results = curs.execute(query, insert_data)
                curs.close()

            except mysql.connector.Error as error:
                print(error)
                results = error

            self.conn.commit()

            return results

    def close_connections(self):
        self.conn.close()

    def get_all_records(self):
        query = "select * from tbl_times order by id desc"
        records = self.db_curs(query)
        self.close_connections()
        return records

    def get_last_record(self):
        date = {'date': datetime.today().strftime('%Y-%m-%d')}
        print(date)
        query = "select * from tbl_times where date = %(date)s and current_feed is True;"
        record = self.db_curs(query=query, data=date)
        print(record)
        return record

    def new_entry(self, **kwargs):
        query = ""
        print(kwargs)
        if 'start_feed' in kwargs.keys():
            query = "insert into tbl_times (start_feed, date, current_feed, notes) " \
                    "values (%(start_feed)s, %(date)s, True, %(notes)s)"
        elif 'end_feed' in kwargs.keys():
            query = "update tbl_times set end_feed = %(end_feed)s, " \
                    "current_feed = False, notes = %(notes)s where id = %(id)s"
        elif 'bottle' in kwargs.keys():
            query = 'insert into tbl_times (start_feed, end_feed, date, current_feed, notes) ' \
                    'values (%(bottle)s, %(bottle)s, %(date)s, False, %(notes)s)'
        elif 'poop_time' in kwargs.keys():
            query = "insert into tbl_times (poop_time, date, notes) values (%(poop_time)s, %(date)s, %(notes)s)"
        elif 'pee_time' in kwargs.keys():
            query = "insert into tbl_times (pee_time, date, notes) values (%(pee_time)s, %(date)s, %(notes)s)"

        result = self.db_curs(query, insert_data=kwargs)
        print(result)
        self.close_connections()
        return result


if __name__ == "__main__":
    db = DataBase()
    # result = db.get_all_records()
    # result = db.new_entry(start_feed='11:30', date='2019-07-11')
    # result = db.get_last_record()
    # print(result)
