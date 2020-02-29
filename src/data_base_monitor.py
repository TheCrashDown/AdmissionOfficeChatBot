import psycopg2


class DataBaseMonitor:
    def __init__(self, db_name, db_user, password):
        self.data_base = psycopg2.connect(dbname=db_name, user=db_user,
                                          password=password, host='localhost')
        self.data_base.autocommit = True

        cursor = self.data_base.cursor()

        cursor.execute("Create table if not exists LADDER ("
                       "EMAIL varchar(100) PRIMARY KEY, "
                       "NAME TEXT NOT NULL, "
                       "SURNAME TEXT NOT NULL, "
                       "SUMM INTEGER DEFAULT 0, "
                       "PHYSICS INTEGER DEFAULT 0, "
                       "MATHS INTEGER DEFAULT 0, "
                       "INF INTEGER DEFAULT 0, "
                       "RUS INTEGER DEFAULT 0, "
                       "PHYSTECH_SCHOOL INTEGER DEFAULT -1, "
                       "DIRECTION TEXT "
                       ");")

        cursor.execute("Create table if not exists USR ("
                       "EMAIL varchar(100) PRIMARY KEY, "
                       "CHATID INTEGER UNIQUE "
                       ");")

        cursor.close()

    def check_user(self, chat_id):
        cursor = self.data_base.cursor()

        cursor.execute("Select * "
                       "from USR "
                       "where CHATID = %(user_id)s",
                       {'user_id': chat_id})

        if cursor.row_count == 0:
            cursor.close()
            return 0

        cursor.close()
        return 1

    def reg_user(self, chat_id, email):
        cursor = self.data_base.cursor()

        cursor.execute("Insert into USR (EMAIL, CHATID) "
                       "values(%(user_id)s, %(email)s )",
                       {'user_id': chat_id, 'email': email})

        cursor.close()
