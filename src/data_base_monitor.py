import psycopg2


class DataBaseMonitor:
    def __init__(self, db_name, db_user, password):
        self.data_base = psycopg2.connect(dbname=db_name, user=db_user,
                                          password=password, host='localhost')
        self.data_base.autocommit = True

        cursor = self.data_base.cursor()

        cursor.execute("Create table if not exists LADDER ("
                       "EMAIL varchar(100) PRIMARY KEY, "
                       "FIRST_NAME TEXT NOT NULL, "
                       "SURNAME TEXT NOT NULL, "
                       "SUMMARY INTEGER DEFAULT 0, "
                       "CERTIFICATE BOOLEAN DEFAULT False, "
                       "PHYSTECH_SCHOOL INTEGER DEFAULT -1, "
                       "DIRECTION TEXT "
                       ");")

        cursor.close()

    def get_number_of_people_above(self, chat_id):

        with self.data_base.cursor() as cursor:

            cursor.execute("SELECT * "
                           "FROM ladder inner join abitu "
                           "on abitu.email = ladder.email "
                           "WHERE user_id = %(user_id)s);",
                           {'user_id': chat_id})

            if cursor.rowcount:
                cursor.execute("SELECT Count(*) "
                               "FROM ladder "
                               "WHERE summary > "
                               "(SELECT summary "
                               "FROM ladder inner join abitu "
                               "on abitu.email = ladder.email "
                               "WHERE user_id = %(user_id)s);",
                               {'user_id': chat_id})
                return int(cursor.fetchone()[0])
            else:
                return 5555


    def get_summary(self, chat_id):
        with self.data_base.cursor() as cursor:
            cursor.execute("SELECT summary"
                           "FROM ladder"
                           "WHERE user_id = %(user_id)s);",
                           {'user_id': chat_id})
            return cursor.fetchone()[0]


    def get_number_of_people_above_with_certificate(self, chat_id):

        with self.data_base.cursor() as cursor:

            cursor.execute("SELECT * "
                           "FROM ladder inner join abitu "
                           "on abitu.email = ladder.email "
                           "WHERE user_id = %(user_id)s);",
                           {'user_id': chat_id})

            if cursor.rowcount:
                cursor.execute("SELECT Count(*) "
                               "FROM ladder "
                               "WHERE summary > "
                               "(SELECT summary "
                               "FROM ladder inner join abitu "
                               "on abitu.email = ladder.email "
                               "WHERE user_id = %(user_id)s)"
                               "AND certificate = True;",
                               {'user_id': chat_id})
                return int(cursor.fetchone()[0]) + 1
            else:
                return 5555

    def number_of_people(self):

        with self.data_base.cursor() as cursor:
            cursor.execute("SELECT Count(*)"
                           "FROM ladder;")
            return cursor.fetchone()[0]
