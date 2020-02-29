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

        cursor.close()

    def get_position(self, chat_id):
        cursor = self.data_base.cursor()

        cursor.execute("Select * "
                       "from USR "
                       "where CHATID = %(user_id)s",
                       {'user_id': chat_id})

        email = cursor.fetchone()

        cursor.execute("Select * "
                       "from LADDER "
                       "where EMAIL = %(user_id)s",
                       {'user_id': email})

        pidor = cursor.fetchone()

        return pidor

        cursor.close()
