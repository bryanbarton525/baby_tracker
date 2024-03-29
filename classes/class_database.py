import mysql.connector
import json
import hashlib


class DataBase:
    """
    Class to manage different database connections and queries.
    """

    def __init__(self):
        with open('/home/tracker/configs/db_conn.json') as conf_file:
            self.conf = json.load(conf_file)
        try:
            self.conn = mysql.connector.connect(**self.conf['database_creds'])

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
                curs.execute(query, insert_data)
                curs.close()
                results = 'Success'

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

    def get_last_record(self, **kwargs):
        print(kwargs)
        query = "select * from tbl_times where current_feed is True;"
        record = self.db_curs(query=query, data=kwargs)
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
        elif 'both' in kwargs.keys():
            query = "insert into tbl_times (poop_time, pee_time, date, notes) " \
                    "values (%(both)s, %(both)s, %(date)s, %(notes)s)"

        result = self.db_curs(query, insert_data=kwargs)
        print(result)
        self.close_connections()
        return result

    def validate(self, **kwargs):
        query = "select password from tbl_users where username = %(username)s"
        results = self.db_curs(query, data=kwargs)
        hashed_password = results[0]['password']
        print(hashed_password)
        self.close_connections()
        return hashed_password == hashlib.md5((self.conf['salt'] + kwargs['password']).encode()).hexdigest()

    def add_user(self, **kwargs):
        kwargs.update({'password': hashlib.md5((self.conf['salt'] + kwargs['password']).encode()).hexdigest()})
        query = "insert into tbl_users (username, password) values (%(username)s, %(password)s)"
        results = self.db_curs(query, insert_data=kwargs)
        self.close_connections()
        return results


if __name__ == '__name__':
    db = DataBase()
    print(db.conf)
