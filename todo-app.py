from PyQt5.QtWidgets import QHBoxLayout, QTextEdit
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QWidget, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QStandardItemModel, QStandardItem, QBrush, QColor

class ToDoList(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('To-Do List')
        layout = QVBoxLayout()

        # Widgets
        self.list_widget = QListWidget()
        self.add_button = QPushButton('Add Task')
        self.remove_button = QPushButton('Remove Task')
        self.mark_button = QPushButton('Mark as Completed')
        self.save_button = QPushButton('Save To File')
        self.load_button = QPushButton('Load From File')
        self.edit_button = QPushButton('Edit Task')
        self.prioritize_button = QPushButton('Prioritize Task')
        self.sort_button = QPushButton('Sort Tasks')
        self.search_button = QPushButton('Search Task')  # New button for searching tasks

        # Connect buttons to their functions
        self.add_button.clicked.connect(self.add_task)
        self.remove_button.clicked.connect(self.remove_task)
        self.mark_button.clicked.connect(self.mark_completed)
        self.save_button.clicked.connect(self.save_to_file)
        self.load_button.clicked.connect(self.load_from_file)
        self.edit_button.clicked.connect(self.edit_task)
        self.prioritize_button.clicked.connect(self.prioritize_task)
        self.sort_button.clicked.connect(self.sort_tasks)
        self.search_button.clicked.connect(self.search_task)  # Connect the new button to its function

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget)
        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.remove_button)
        left_layout.addWidget(self.mark_button)
        left_layout.addWidget(self.save_button)
        left_layout.addWidget(self.load_button)
        left_layout.addWidget(self.edit_button)
        left_layout.addWidget(self.prioritize_button)
        left_layout.addWidget(self.sort_button)
        left_layout.addWidget(self.search_button)  # Add the new button to the layout
        
        right_layout = QVBoxLayout()
        self.task_details_widget = QTextEdit()
        self.task_details_widget.setPlaceholderText('Select a task to view details...')
        right_layout.addWidget(self.task_details_widget)
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_task(self):
        new_task, ok = QInputDialog.getText(self, 'Add Task', 'Enter task:')
        if ok and new_task != '':
            item = QListWidgetItem(new_task)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # Makes the item checkable
            item.setCheckState(Qt.Unchecked)  # Default state is unchecked
            self.list_widget.addItem(item)

    def remove_task(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            row = self.list_widget.row(current_item)
            self.list_widget.takeItem(row)

    def mark_completed(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            current_item.setCheckState(Qt.Checked)

    def save_to_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save To-Do List", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                for row in range(self.list_widget.count()):
                    item = self.list_widget.item(row)
                    task_text = item.text()
                    task_status = "completed" if item.checkState() == Qt.Checked else "not completed"
                    file.write(f'{task_text};{task_status}\n')

    def load_from_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open To-Do List", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.list_widget.clear()
                for line in file:
                    task_text, task_status = line.strip().split(';')
                    item = QListWidgetItem(task_text)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    if task_status == "completed":
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                    self.list_widget.addItem(item)

    def edit_task(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            new_task, ok = QInputDialog.getText(self, 'Edit Task', 'Enter new task details:', text=current_item.text())
            if ok and new_task != '':
                current_item.setText(new_task)

    def prioritize_task(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            current_row = self.list_widget.row(current_item)
            self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(0, current_item)

    def sort_tasks(self):
        tasks = []
        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            tasks.append((item.text(), item.checkState()))
        tasks.sort()
        self.list_widget.clear()
        for task_text, task_state in tasks:
            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(task_state)
            self.list_widget.addItem(item)

    def search_task(self):  # New function for searching tasks
        search_term, ok = QInputDialog.getText(self, 'Search Task', 'Enter search term:')
        if ok and search_term != '':
            for row in range(self.list_widget.count()):
                item = self.list_widget.item(row)
                if search_term.lower() in item.text().lower():
                    item.setBackground(QBrush(QColor('yellow')))
                else:
                    item.setBackground(QBrush(QColor('white')))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoList()
    window.show()
    sys.exit(app.exec_())
