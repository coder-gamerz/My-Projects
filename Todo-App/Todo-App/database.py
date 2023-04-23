import sqlite3

class Database:
    def __init__(self, db) -> None:
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS todos(id INTEGER PRIMARY KEY, todo_item text, created_at text, updated_at text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM todos")
        rows = self.cur.fetchall()
        return rows

    def insert(self, todo):
        self.cur.execute("INSERT INTO todos VALUES (NULL, ?, datetime('now'), datetime('now'))", (todo,))
        self.conn.commit()

    def update(self, id,todo_item):
        self.cur.execute("UPDATE todos SET todo_item = ?, updated_at = datetime('now') WHERE id = ?", (todo_item, id))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM todos WHERE id = ?", (id,))
        self.conn.commit()

    def __delattr__(self) -> None:
        self.conn.close()