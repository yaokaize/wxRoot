class JournalService:
    def __init__(self):
        self.__table = 'tb_journal'

    def insert_journal(self, pgUtil, journal):
        sql = 'insert into yangming.tb_journal (wx_id, money, create_time) values ("%s", "%s", "%s")' % (
        journal.get("wx_id"), journal.get("money"), journal.get("create_time"))
        pgUtil.execute(sql)
