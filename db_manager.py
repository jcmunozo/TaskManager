import sqlite3

def init_database():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         progress INTEGER DEFAULT 0)
    ''')
    conn.commit()
    return conn

def add_task(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, progress) VALUES (?, ?)", (name, 0))
    conn.commit()

def get_tasks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, progress FROM tasks")
    return cursor.fetchall()

def get_task_progress(conn, task_id):
    cursor = conn.cursor()
    cursor.execute("SELECT progress FROM tasks WHERE id = ?", (task_id,))
    return cursor.fetchone()[0]

def update_task_progress(conn, task_id, progress):
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET progress = ? WHERE id = ?", (progress, task_id))
    conn.commit()

def delete_task(conn, task_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
