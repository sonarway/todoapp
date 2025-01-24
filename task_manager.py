from database import Database
from timer import Timer

class TaskManager:
    def __init__(self):
        self.db = Database()
        self.timer = Timer()

    def add_task(self, task):
        self.db.add_task(task)

    def get_tasks(self):
        return self.db.get_tasks()

    def get_task_id(self, task_name):
        return self.db.get_task_id(task_name)

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        return self.timer.stop()

    def update_time_spent(self, task_id, time_spent):
        self.db.update_task_time(task_id, time_spent)

    def mark_task_completed(self, task_id):
        self.db.update_task_status(task_id, 1)  # Mark the task as completed
