import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def init_db():
    conn = sqlite3.connect("tasks_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_to_db(title, desc, status):
    conn = sqlite3.connect("tasks_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (title, desc, status))
    conn.commit()
    conn.close()

def update_in_db(task_id, title, desc, status):
    conn = sqlite3.connect("tasks_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=?, description=?, status=? WHERE id=?", (title, desc, status, task_id))
    conn.commit()
    conn.close()

def delete_from_db(task_id):
    conn = sqlite3.connect("tasks_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def fetch_tasks(search_query=""):
    conn = sqlite3.connect("tasks_db.sqlite")
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?", (f'%{search_query}%', f'%{search_query}%'))
    else:
        cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Мои Задачи")
        self.root.geometry("750x500")
        
        self.task_id = None
        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Новая")

        
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(fill="x", padx=10)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        tk.Entry(input_frame, textvariable=self.title_var, width=30).grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Описание:").grid(row=0, column=2, sticky="w")
        tk.Entry(input_frame, textvariable=self.desc_var, width=30).grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Статус:").grid(row=1, column=0, sticky="w", pady=5)
        status_options = ["Новая", "В процессе", "Готово"]
        self.status_menu = ttk.Combobox(input_frame, textvariable=self.status_var, values=status_options, state="readonly")
        self.status_menu.grid(row=1, column=1, padx=5, sticky="w")

    
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(btn_frame, text="Добавить", bg="#50fa7b", command=self.add_task, width=10).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Обновить", bg="#363f5c", command=self.update_task, width=10).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Удалить", bg="#d7f8f3", command=self.delete_task, width=10).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Найти", bg="#ccffd5", command=self.search_task, width=10).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Сброс/Все", command=self.refresh_table, width=10).pack(side="left", padx=2)


        columns = ("id", "title", "description", "status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("description", text="Описание")
        self.tree.heading("status", text="Статус")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=150)
        self.tree.column("description", width=250)
        self.tree.column("status", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        self.refresh_table()

    def refresh_table(self, query=""):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in fetch_tasks(query):
            self.tree.insert("", "end", values=row)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
    
        item = self.tree.item(selected[0])
        val = item['values']
        

        self.task_id = val[0]         
        self.title_var.set(val[1])    
        self.desc_var.set(val[2])     
        self.status_var.set(val[3])   

    def add_task(self):
        if self.title_var.get().strip():
            add_to_db(self.title_var.get(), self.desc_var.get(), self.status_var.get())
            self.refresh_table()
            self.clear_fields()
        else:
            messagebox.showwarning("Ошибка", "Введите название задачи")

    def update_task(self):
        if self.task_id:
            update_in_db(self.task_id, self.title_var.get(), self.desc_var.get(), self.status_var.get())
            self.refresh_table()
            self.clear_fields()
        else:
            messagebox.showwarning("Ошибка", "Выберите задачу в таблице")

    def delete_task(self):
        if self.task_id:
            delete_from_db(self.task_id)
            self.refresh_table()
            self.clear_fields()
        else:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления")

    def search_task(self):
        self.refresh_table(self.title_var.get())

    def clear_fields(self):
        self.task_id = None
        self.title_var.set("")
        self.desc_var.set("")
        self.status_var.set("Новая")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
