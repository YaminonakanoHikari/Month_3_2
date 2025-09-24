import sqlite3
from db import queries
from config import path_db


def init_db():
    """Создаём таблицу, если её ещё нет"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASKS)
    conn.commit()
    conn.close()


def add_task(task_text: str) -> int:
    """Добавляем задачу, возвращаем её id"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task_text,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_tasks(filter_type: str = "all"):
    """Получаем список задач с фильтрацией"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == "completed":
        cursor.execute(queries.SELECT_TASKS_COMPLETED)
    elif filter_type == "uncompleted":
        cursor.execute(queries.SELECT_TASKS_UNCOMPLETED)
    else:
        cursor.execute(queries.SELECT_TASKS)

    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(task_id: int, task_text: str = None, completed: int = None):
    """Обновляем задачу: либо текст, либо статус"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if task_text is not None:  
        cursor.execute(queries.UPDATE_TASK, (task_text, task_id))

    if completed is not None: 
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))

    conn.commit()
    conn.close()


def delete_task(task_id: int):
    """Удаляем задачу по id"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()
