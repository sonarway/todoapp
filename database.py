import sqlite3

class Database:
    def __init__(self, db_name="tasks_cb.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    time_spent INTEGER DEFAULT 0,
                    completed INTEGER DEFAULT 0  -- New column to track completion
                )
            """)

    def add_task(self, task):
        with self.conn:
            self.conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))

    def get_tasks(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM tasks").fetchall()

    def get_task_id(self, task_name):
        with self.conn:
            result = self.conn.execute("SELECT id FROM tasks WHERE task = ?", (task_name,)).fetchone()
            return result[0] if result else None

    def update_task_time(self, task_id, time_spent):
        with self.conn:
            self.conn.execute("UPDATE tasks SET time_spent = time_spent + ? WHERE id = ?", (time_spent, task_id))

    def update_task_status(self, task_id, completed):
        with self.conn:
            self.conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    
    def mark_task_completed(self, task_id):
        with self.conn:
            self.conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))

