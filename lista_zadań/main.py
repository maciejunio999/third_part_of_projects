from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QCheckBox, QMessageBox
from PyQt5.QtGui import QColor
import pickle
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.label_title = QLabel("Aplikacja Zarządzania Zadaniami")
        self.label_title.setStyleSheet("font-size: 20px; color: white; background-color: #3498db; padding: 10px;")

        self.button_add_task = QPushButton("Dodaj zadanie")
        self.button_add_task.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")

        self.button_list_tasks = QPushButton("Lista zadań")
        self.button_list_tasks.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")

        self.button_save_tasks = QPushButton("Zapisz zadania")
        self.button_save_tasks.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.button_add_task)
        layout.addWidget(self.button_list_tasks)
        layout.addWidget(self.button_save_tasks)

        self.setLayout(layout)

        self.button_add_task.clicked.connect(self.on_button_add_task_clicked)
        self.button_list_tasks.clicked.connect(self.on_button_list_tasks_clicked)
        self.button_save_tasks.clicked.connect(self.on_button_save_tasks_clicked)

        # Create an instance of ListTasksDialog
        self.list_tasks_dialog = ListTasksDialog()
        self.add_task_dialog = None

        # Load tasks from file
        self.load_tasks()

    def on_button_add_task_clicked(self):
        # Check if the AddTaskDialog instance exists
        if self.add_task_dialog is None:
            self.add_task_dialog = AddTaskDialog(self.list_tasks_dialog)

        self.add_task_dialog.show()

    def on_button_list_tasks_clicked(self):
        self.list_tasks_dialog.show()

    def on_button_save_tasks_clicked(self):
        # Save tasks to file
        self.save_tasks()

    def load_tasks(self):
        try:
            with open('tasks.pkl', 'rb') as file:
                tasks = pickle.load(file)
                for task, is_done in tasks:
                    self.list_tasks_dialog.add_task(task, is_done)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        tasks = self.list_tasks_dialog.get_tasks()
        with open('tasks.pkl', 'wb') as file:
            pickle.dump(tasks, file)


class AddTaskDialog(QDialog):
    def __init__(self, list_tasks_dialog):
        super().__init__()

        self.label_title = QLabel("Dodaj zadanie")
        self.label_title.setStyleSheet("font-size: 16px; color: #2ecc71;")

        self.line_edit_task = QLineEdit()
        self.button_add = QPushButton("Dodaj")
        self.button_add.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.line_edit_task)
        layout.addWidget(self.button_add)

        self.setLayout(layout)

        self.button_add.clicked.connect(self.on_button_add_clicked)

        # Reference to the ListTasksDialog
        self.list_tasks_dialog = list_tasks_dialog

    def on_button_add_clicked(self):
        task = self.line_edit_task.text().strip()
        if not task:
            QMessageBox.warning(self, "Błąd", "Nazwa zadania nie może być pusta.")
            return

        self.list_tasks_dialog.add_task(task)
        self.line_edit_task.clear()
        self.close()


class ListTasksDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()
        self.checkbox_show_done = QCheckBox("Pokaż wykonane zadania")
        self.checkbox_show_done.setStyleSheet("color: #2ecc71;")

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox_show_done)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        self.checkbox_show_done.stateChanged.connect(self.on_checkbox_show_done_changed)
        self.show_done = False

    def add_task(self, task, is_done=False):
        item = QListWidgetItem()
        checkbox = QCheckBox("Wykonane")
        checkbox.setChecked(is_done)
        button_remove = QPushButton("Usuń")
        button_remove.setStyleSheet("background-color: #e74c3c; color: white; padding: 5px;")

        # Tworzymy dodatkowy widget do połączenia labela, checkboxa i przycisku
        widget = QWidget()
        h_layout = QHBoxLayout(widget)
        h_layout.addWidget(QLabel(task))
        h_layout.addWidget(checkbox)
        h_layout.addWidget(button_remove)

        # Dodajemy widget do list_widget
        item.setSizeHint(widget.sizeHint())  # Ustawiamy wielkość na podstawie zawartości
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

        # Ukryj wykonane zadania, jeśli show_done jest ustawione na False
        item.setHidden(is_done and not self.show_done)

        # Połącz zdarzenie kliknięcia checkboxa
        checkbox.clicked.connect(lambda: self.on_checkbox_clicked(item))

        # Połącz zdarzenie kliknięcia przycisku usuwania
        button_remove.clicked.connect(lambda: self.on_button_remove_clicked(item))

    def on_checkbox_clicked(self, item):
        checkbox = self.list_widget.itemWidget(item).layout().itemAt(1).widget()
        is_done = checkbox.isChecked()

        if not self.show_done:
            item.setHidden(is_done)

    def on_button_remove_clicked(self, item):
        row = self.list_widget.row(item)
        self.list_widget.takeItem(row)

        # Sprawdź czy usuwane zadanie było wykonane
        widget = self.list_widget.itemWidget(item)
        if widget is not None:
            layout = widget.layout()
            if layout is not None:
                checkbox = layout.itemAt(1).widget()
                if checkbox is not None and checkbox.isChecked():
                    # Jeśli show_done jest ustawione na False i usuwane zadanie jest wykonane,
                    # to musimy ukryć zadanie
                    if not self.show_done:
                        item.setHidden(True)


    def on_checkbox_show_done_changed(self, state):
        self.show_done = state == 2  # 2 oznacza zaznaczone
        self.show_tasks()

    def show_tasks(self):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            is_done = self.list_widget.itemWidget(item).layout().itemAt(1).widget().isChecked()
            item.setHidden(is_done and not self.show_done)

    def get_tasks(self):
        tasks = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            task = self.list_widget.itemWidget(item).layout().itemAt(0).widget().text()
            is_done = self.list_widget.itemWidget(item).layout().itemAt(1).widget().isChecked()
            tasks.append((task, is_done))
        return tasks


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Aplikacja Zarządzania Zadaniami")
    window.setGeometry(100, 100, 400, 300)  # Ustawienia szerokości i wysokości okna
    window.show()

    sys.exit(app.exec_())
