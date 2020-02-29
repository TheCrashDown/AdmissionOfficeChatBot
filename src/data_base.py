import psycopg2

class DataBase:
    def __init__(self, db_name, db_user, password):
        self.data_base = psycopg2.connect(dbname=db_name, user=db_user,
                                          password=password, host='localhost')
        self.data_base.autocommit = True

        cursor = self.data_base.cursor()

        cursor.execute('Create table if not exists ABITU ( \
                        USER_ID varchar(20) primary key, \
                        STATUS TEXT, \
                        EMAIL varchar(100)\
                        );')

