import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QWidget, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QStandardItemModel, QStandardItem

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

        # Connect buttons to their functions
        self.add_button.clicked.connect(self.add_task)
        self.remove_button.clicked.connect(self.remove_task)
        self.mark_button.clicked.connect(self.mark_completed)
        self.save_button.clicked.connect(self.save_to_file)
        self.load_button.clicked.connect(self.load_from_file)

        # Add widgets to layout
        layout.addWidget(self.list_widget)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.mark_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def add_task(self):
        new_task, _ = QInputDialog.getText(self, 'Add Task', 'Task:')
        if new_task:
            item = QListWidgetItem(new_task)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable) # Makes the item checkable
            item.setCheckState(Qt.Unchecked) # Default state is unchecked
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoList()
    window.show()
    sys.exit(app.exec_())
