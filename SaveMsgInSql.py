import pymysql


class SaveMsgInSql():
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.conn = None
        self.cur = None

    def conn_sql(self):
        self.conn = pymysql.connect(self.host, self.user, self.password, self.database)
        self.cur = self.conn.cursor()

    def conn_savemsg(self):
        pass

    def conn_close(self):
        self.cur.close()
        self.conn.close()


