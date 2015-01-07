import psycopg2
import psycopg2.extras
from config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT


class DBHelper(object):
    conn = None

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(database=DB_NAME,
                                    user=DB_USER,
                                    password=DB_PASSWORD,
                                    host=DB_HOST,
                                    port=DB_PORT)

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e

    def disconnect(self):
        self.conn.close()

    def result_to_dict(self, names, values):
        result = {}
        for i in range(0, len(values)):
            result[names[i]] = values[i]
        return result

    def common(self, proc_name, type, args):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.callproc(proc_name, args)
        attr = getattr(cur, type, 'fetchall')
        col_names = [desc[0] for desc in cur.description]
        values = attr()
        if type == 'fetchone':
            result = self.result_to_dict(col_names, values)
        else:
            result = [self.result_to_dict(col_names, value) for value in values]
        cur.close()
        return result

    def search(self, proc_name, args):
        return self.common(proc_name, 'fetchall', args)

    def list(self, proc_name):
        return self.common(proc_name, 'fetchall', ())

    def get(self, proc_name, args):
        return self.common(proc_name, 'fetchone', args)

    def create(self, proc_name, args):
        return self.common(proc_name, 'fetchone', args)

    def update(self, proc_name, args):
        return self.common(proc_name, 'fetchone', args)

