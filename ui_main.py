from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSizePolicy, QProgressBar,
                             QScrollArea, QInputDialog, QMessageBox, QDialog, QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen
import db_manager

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Tareas")
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

        # Configuración del panel izquierdo
        left_panel = self.create_left_panel()
        layout.addWidget(left_panel)

        # Configuración del panel derecho
        right_panel = self.create_right_panel()
        layout.addWidget(right_panel)

        self.add_task_btn.clicked.connect(self.add_task)
        self.close_app_btn.clicked.connect(self.close)

        self.load_tasks()
        self.setFixedSize(self.size())

    def create_left_panel(self):
        left_panel = QWidget()
        left_panel.setFixedWidth(200)
        left_layout = QVBoxLayout(left_panel)

        self.add_task_btn = QPushButton("Agregar Tarea")
        self.add_task_btn.setFixedHeight(40)
        self.close_app_btn = QPushButton("Cerrar Aplicación")
        self.close_app_btn.setFixedHeight(40)

        left_layout.addWidget(self.add_task_btn)
        left_layout.addStretch()
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
        name, ok = QInputDialog.getText(self, "Nueva Tarea", "Nombre de la tarea:")
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

        update_btn = QPushButton("Actualizar")
        update_btn.setFixedSize(80, 30)
        update_btn.clicked.connect(lambda checked, tid=task_id: self.update_task(tid))
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("Eliminar")
        delete_btn.setFixedSize(80, 30)
        delete_btn.clicked.connect(lambda checked, tid=task_id: self.delete_task(tid))
        button_layout.addWidget(delete_btn)

        task_layout.addWidget(button_container)

        return task_widget

    def update_task(self, task_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar Progreso")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout(dialog)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)

        current_progress = db_manager.get_task_progress(self.conn, task_id)
        slider.setValue(current_progress)

        value_label = QLabel(f"Progreso: {current_progress}%")

        slider.valueChanged.connect(lambda: value_label.setText(f"Progreso: {slider.value()}%"))

        button_box = QHBoxLayout()
        accept_btn = QPushButton("Aceptar")
        cancel_btn = QPushButton("Cancelar")
        accept_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)

        button_box.addWidget(accept_btn)
        button_box.addWidget(cancel_btn)

        layout.addWidget(QLabel("Arrastra el slider para ajustar el progreso:"))
        layout.addWidget(slider)
        layout.addWidget(value_label)
        layout.addLayout(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            db_manager.update_task_progress(self.conn, task_id, slider.value())
            self.load_tasks()

    def delete_task(self, task_id):
        reply = QMessageBox.question(self, "Confirmar Eliminación",
                                     "¿Estás seguro de que deseas eliminar esta tarea?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            db_manager.delete_task(self.conn, task_id)
            self.load_tasks()
    
    def closeEvent(self, event):
        self.conn.close()
