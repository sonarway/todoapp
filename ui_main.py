from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer
from task_manager import TaskManager

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.current_task_id = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_label)
        self.init_ui()
        self.elapsed_time = 0

    def init_ui(self):
        self.setWindowTitle("to-do")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color: #EADDCA; font-family: 'Roboto'; font-size: 14px;")

        layout = QVBoxLayout()

        # Task Input
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("task")
        layout.addWidget(self.task_input)

        # Add Task Button
        self.add_button = QPushButton("add task")
        self.add_button.setStyleSheet("background-color: #6F4E37; color: #ffffff;")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        # To-Do Task List
        self.todo_list = QListWidget()
        layout.addWidget(QLabel("to-do"))
        layout.addWidget(self.todo_list)

        # Completed Task List
        self.completed_list = QListWidget()
        layout.addWidget(QLabel("yay good job"))
        layout.addWidget(self.completed_list)

        # Timer Label
        self.timer_label = QLabel("timer: 00:00:00")
        layout.addWidget(self.timer_label)

        # Start/Stop Timer Buttons
        self.start_timer_btn = QPushButton("start timer")
        self.start_timer_btn.clicked.connect(self.start_timer)
        self.start_timer_btn.setStyleSheet("background-color: #6F4E37; color: #ffffff;")
        layout.addWidget(self.start_timer_btn)

        self.stop_timer_btn = QPushButton("stop timer")
        self.stop_timer_btn.clicked.connect(self.stop_timer)
        self.stop_timer_btn.setStyleSheet("background-color: #6F4E37; color: #ffffff;")
        layout.addWidget(self.stop_timer_btn)

        self.setLayout(layout)
        self.load_tasks()

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            self.task_manager.add_task(task)
            self.task_input.clear()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "warning", "task cannot be empty :(")

    def load_tasks(self):
        self.todo_list.clear()
        self.completed_list.clear()

        # Load all tasks from the database
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            if task[3] == 0:  # If task is not completed
                self.todo_list.addItem(f"{task[1]} - {task[2]} seconds")
            else:  # If task is completed
                self.completed_list.addItem(f"{task[1]} - {task[2]} seconds")

    def start_timer(self):
        if not self.todo_list.selectedItems():
            QMessageBox.warning(self, "warning", "please select a task first :(")
            return
        # Get the selected task ID
        selected_item = self.todo_list.selectedItems()[0]
        task_text = selected_item.text().split(" - ")[0]
        self.current_task_id = self.task_manager.get_task_id(task_text)
        self.task_manager.start_timer()
        self.elapsed_time = 0
        self.timer.start(1000)  # Update every second

    def stop_timer(self):
        if self.current_task_id is not None:
            elapsed_time = self.task_manager.stop_timer()
            self.timer.stop()
            self.task_manager.update_time_spent(self.current_task_id, elapsed_time)
            self.task_manager.mark_task_completed(self.current_task_id)
            self.elapsed_time = 0
            self.timer_label.setText(f"{elapsed_time} seconds")
            self.load_tasks()  # Reload tasks after moving it to completed
        else:
            QMessageBox.warning(self, "warning", "please select a task first :(")

    def update_timer_label(self):
        self.elapsed_time += 1
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_label.setText(f"timer: {hours:02}:{minutes:02}:{seconds:02}")
