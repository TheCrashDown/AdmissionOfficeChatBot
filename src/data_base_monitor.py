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
                           "WHERE user_id = %(user_id)s;",
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
            cursor.execute("SELECT summary "
                           "FROM ladder inner join abitu "
                           "on abitu.email = ladder.email "
                           "WHERE user_id = %(user_id)s;",
                           {'user_id': chat_id})
            ret = cursor.fetchone()
            if ret is None:
                return 0 # hui
            else:
                return int(ret[0])


    def get_number_of_people_above_with_certificate(self, chat_id):

        with self.data_base.cursor() as cursor:

            cursor.execute("SELECT * "
                           "FROM ladder inner join abitu "
                           "on abitu.email = ladder.email "
                           "WHERE user_id = %(user_id)s;",
                           {'user_id': chat_id})

            if cursor.rowcount:
                cursor.execute("SELECT Count(*) "
                               "FROM ladder "
                               "WHERE summary > "
                               "(SELECT summary "
                               "FROM ladder inner join abitu "
                               "on abitu.email = ladder.email "
                               "WHERE user_id = %(user_id)s) "
                               "AND certificate = True;",
                               {'user_id': chat_id})
                return int(cursor.fetchone()[0])
            else:
                return 5555

    def number_of_people(self):

        with self.data_base.cursor() as cursor:
            cursor.execute("SELECT Count(*)"
                           "FROM ladder;")
            return cursor.fetchone()[0]

    def receive_ladder(self, chat_id):

        with self.data_base.cursor() as cursor:

            cursor.execute("SELECT row_number "
                           "FROM (SELECT *, row_number() over (ORDER BY summary DESC) from ladder) t "
                           "inner join abitu on t.email = abitu.email where user_id = %(user_id)s",
                           {'user_id': chat_id})

            position = cursor.fetchone()[0]

            cursor.execute("with t as "
                           "(SELECT row_number "
                           "FROM (SELECT *, row_number() over (ORDER BY summary DESC) from ladder) t "
                           "inner join abitu on t.email = abitu.email where user_id = %(user_id)s)"
                           "Select rn, first_name, surname, summary, certificate "
                           "from (SELECT *, row_number() over (ORDER BY summary DESC) as rn from ladder) a "
                           "cross join t where rn >= (row_number - 2) and rn <= (row_number + 2) "
                           "order by rn;",
                           {'user_id': chat_id})

            return cursor.fetchall(), position
