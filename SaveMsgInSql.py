import pymysql
import ConfigMsg

class SaveMsgInSql():
    def __init__(self):
        self.host = ConfigMsg.host
        self.username = ConfigMsg.username
        self.password = ConfigMsg.password
        self.database = ConfigMsg.database
        self.conn = None
        self.cur = None

    def conn_sql(self):
        self.conn = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database)
        self.cur = self.conn.cursor()

    def conn_get_msg(self):
        sql = "SELECT url_md5 FROM test_save_filedata"
        self.conn_sql()
        self.cur.execute(sql)
        results = list(self.cur.fetchall())
        return results

    def conn_save_msg(self, data):
        try:
            sql = " INSERT INTO test_save_filedata(name, parent_path, url_md5, download_url,create_date) VALUES(%s,%s,%s,%s,%s) "
            self.conn_sql()
            self.cur.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn_close()

    def conn_delete_msg(self, data):
        try:
            sql = "DELETE FROM test_save_filedata WHERE url_md5 = %s"
            self.conn_sql()
            self.cur.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn_close()

    def conn_close(self):
        self.cur.close()
        self.conn.close()




