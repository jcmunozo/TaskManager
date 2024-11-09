import sqlite3
import os
import sys

def get_exe_path():
    if getattr(sys, 'frozen', False):
        # Get the path to the executable
        return os.path.dirname(sys.executable)
    else:
        # On dev, use the path where the script is
        return os.path.dirname(os.path.abspath(__file__))

def init_database():
    try:
        # get the path to the exe
        exe_dir = get_exe_path()
        db_path = os.path.join(exe_dir, "tasks.db")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             progress INTEGER DEFAULT 0)
        ''')
        conn.commit()
        return conn
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return None

def add_task(conn, name):
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (name, progress) VALUES (?, ?)", (name, 0))
        conn.commit()
    except Exception as e:
        print(f"error initializing database: {e}")
        conn.rollback()

def get_tasks(conn):
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, progress FROM tasks")
        return cursor.fetchall()
    except Exception as e:
        print(f"error getting tasks: {e}")
        return []

def get_task_progress(conn, task_id):
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT progress FROM tasks WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"error getting progress: {e}")
        return None

def update_task_progress(conn, task_id, progress):
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET progress = ? WHERE id = ?", (progress, task_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating progress: {e}")
        conn.rollback()

def delete_task(conn, task_id):
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting task: {e}")
        conn.rollback()

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
