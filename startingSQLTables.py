import sqlite3 as sql


class startingSQLTables:
    def __init__(self):
        self.conn = sql.connect("expenseT.db")
        self.cursor_obj = self.conn.cursor()
        table_users = "CREATE TABLE IF NOT EXISTS users(username VARCHAR PRIMARY KEY, email VARCHAR,password VARCHAR)"
        table_transactions = "CREATE TABLE IF NOT EXISTS transactions " \
                             "(id INTEGER PRIMARY KEY AUTOINCREMENT,username VARCHAR NOT NULL, typeOf VARCHAR, category VARCHAR, amount DOUBLE, note VARCHAR" \
                             ",dateOf VARCHAR, FOREIGN KEY(username) REFERENCES  users(username))"

        table_categories = "CREATE TABLE IF NOT EXISTS categories(username VARCHAR, typeOf VARCHAR,nameOf VARCHAR, UNIQUE(username,nameOf))"
        default_categories = [
            ('default', 'income', 'paycheck'),
            ('default', 'income', 'investment'),
            ('default', 'income', 'bonus'),
            ('deault', 'expense', 'education'),
            ('default', 'expense', 'shopping'),
            ('default', 'expense', 'rent'),
            ('default', 'expense', 'food')
        ]

        self.cursor_obj.execute(table_users)
        self.cursor_obj.execute(table_transactions)
        self.cursor_obj.execute(table_categories)
        insert_default_categories = self.cursor_obj.executemany("INSERT OR IGNORE INTO categories VALUES(?,?,?)",
                                                                default_categories)
        self.conn.commit()
        self.conn.close()
