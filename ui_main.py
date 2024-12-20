from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSizePolicy, QProgressBar,
                             QScrollArea, QInputDialog, QMessageBox, QDialog, QSlider, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen
import db_manager

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setMinimumSize(800, 600)
        self.setBaseSize(800, 600)
        self.resize(800, 600)

        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)

        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.setGeometry(x, y, 1000, 500)

        self.conn = db_manager.init_database()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        # Left panel configuration
        left_panel = self.create_left_panel()
        layout.addWidget(left_panel)

        # Right panel configuration
        right_panel = self.create_right_panel()
        layout.addWidget(right_panel)

        self.add_task_btn.clicked.connect(self.add_task)
        self.close_app_btn.clicked.connect(self.close)

        self.light_mode_checkbox.stateChanged.connect(self.toggle_theme)

        self.base_style = """
            QPushButton {
                min-height: 27px;
            }
        """

        self.dark_style = """
            QMainWindow, QDialog {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #424242;
                color: #ffffff;
                min-height: 27px;
            }
            QPushButton:hover {
                background-color: #525252;
            }
            QLabel {
                color: #ffffff;
            }
            QProgressBar {
                border: 2px solid #424242;
                border-radius: 5px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #2979ff;
                border-radius: 3px;
            }
            QScrollArea {
                border: 1px solid #424242;
            }
            QCheckBox {
                color: #ffffff;
                spacing: 5px;
            }
            QCheckBox::indicator {
                border: 1px solid #2979ff;
                background-color: #424242;
    }
            QInputDialog QLineEdit {
                background-color: #424242;
                color: #ffffff;
                border: 1px solid #525252;
                padding: 5px;
            }
            QMessageBox {
                background-color: #2e2e2e;
            }
        """

        self.setStyleSheet(self.dark_style)
        self.load_tasks()
        self.setFixedSize(self.size())

    def create_left_panel(self):
        left_panel = QWidget()
        left_panel.setFixedWidth(200)
        left_layout = QVBoxLayout(left_panel)

        self.add_task_btn = QPushButton("Add Task")
        self.close_app_btn = QPushButton("Close app")
        self.light_mode_checkbox = QCheckBox("Light Mode")

        left_layout.addWidget(self.add_task_btn)
        left_layout.addStretch()
        left_layout.addWidget(self.light_mode_checkbox)
        left_layout.addWidget(self.close_app_btn)

        return left_panel

    def create_right_panel(self):
        right_panel = QScrollArea()
        right_panel.setWidgetResizable(True)
        right_panel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.tasks_widget = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_layout.setSpacing(10)

        right_panel.setWidget(self.tasks_widget)
        return right_panel

    def add_task(self):
        name, ok = QInputDialog.getText(self, "New Task", "Task name:")
        if ok and name.strip():
            db_manager.add_task(self.conn, name)
            self.load_tasks()

    def load_tasks(self):
        db_manager.clear_layout(self.tasks_layout)
        tasks = db_manager.get_tasks(self.conn)

        for task_id, name, progress in tasks:
            task_widget = self.create_task_widget(task_id, name, progress)
            self.tasks_layout.addWidget(task_widget)
        
        self.tasks_layout.addStretch()

    def create_task_widget(self, task_id, name, progress):
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)
        task_layout.setContentsMargins(5, 5, 5, 5)

        task_label = QLabel(name)
        task_label.setMinimumWidth(150)
        task_layout.addWidget(task_label, 1)

        progress_bar = QProgressBar()
        progress_bar.setFixedWidth(200)
        progress_bar.setFixedHeight(20)
        progress_bar.setValue(progress)
        task_layout.addWidget(progress_bar)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)

        update_btn = QPushButton("Update")
        update_btn.setFixedSize(80, 30)
        update_btn.clicked.connect(lambda checked, tid=task_id: self.update_task(tid))
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setFixedSize(80, 30)
        delete_btn.clicked.connect(lambda checked, tid=task_id: self.delete_task(tid))
        button_layout.addWidget(delete_btn)

        task_layout.addWidget(button_container)

        return task_widget

    def update_task(self, task_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Progress")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout(dialog)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)

        current_progress = db_manager.get_task_progress(self.conn, task_id)
        slider.setValue(current_progress)

        value_label = QLabel(f"Progress: {current_progress}%")

        slider.valueChanged.connect(lambda: value_label.setText(f"Progress: {slider.value()}%"))

        button_box = QHBoxLayout()
        accept_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        accept_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)

        button_box.addWidget(accept_btn)
        button_box.addWidget(cancel_btn)

        layout.addWidget(QLabel("Drag the slider to adjust the progress:"))
        layout.addWidget(slider)
        layout.addWidget(value_label)
        layout.addLayout(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            db_manager.update_task_progress(self.conn, task_id, slider.value())
            self.load_tasks()

    def delete_task(self, task_id):
        reply = QMessageBox.question(self, "confirm deletion",
                                     "¿Are you sure you want to delete this task??",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            db_manager.delete_task(self.conn, task_id)
            self.load_tasks()

    def toggle_theme(self, state):
        if state == Qt.CheckState.Checked.value:
            self.setStyleSheet(self.base_style)
        else:
            self.setStyleSheet(self.dark_style)

    def closeEvent(self, event):
        self.conn.close()
