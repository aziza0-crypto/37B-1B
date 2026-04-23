

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class ShoppingListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список покупок")
        self.root.geometry("600x450")
        
        self.init_db()
        self.create_widgets()
        self.load_data()
        
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def init_db(self):
        self.conn = sqlite3.connect("shopping_list.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                qty INTEGER,
                                category TEXT,
                                bought INTEGER DEFAULT 0)''')
        self.conn.commit()

    def create_widgets(self):
        frame_input = tk.Frame(self.root, pady=10)
        frame_input.pack()

        tk.Label(frame_input, text="Название:").grid(row=0, column=0)
        self.ent_name = tk.Entry(frame_input)
        self.ent_name.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Кол-во:").grid(row=0, column=2)
        self.spin_qty = tk.Spinbox(frame_input, from_=1, to=69, width=5)
        self.spin_qty.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="Категория:").grid(row=0, column=4)
        self.combo_cat = ttk.Combobox(frame_input, values=["Овощи", "Молочные", "Другое"], width=12)
        self.combo_cat.current(2)
        self.combo_cat.grid(row=0, column=5, padx=5)

        frame_btns = tk.Frame(self.root)
        frame_btns.pack(pady=5)

        tk.Button(frame_btns, text="Добавить", command=self.add_item, bg="#e1f5fe").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btns, text="Куплено (+/-)", command=self.toggle_bought).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btns, text="Удалить", command=self.delete_item, fg="red").pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("name", "qty", "cat", "bought"), show='headings')
        self.tree.heading("name", text="Название")
        self.tree.heading("qty", text="Кол-во")
        self.tree.heading("cat", text="Категория")
        self.tree.heading("bought", text="Куплено")
        self.tree.column("qty", width=50, anchor="center")
        self.tree.column("bought", width=80, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.lbl_stats = tk.Label(self.root, text="Всего: 0 | Куплено: 0", font=("Arial", 10, "bold"))
        self.lbl_stats.pack(pady=5)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        
        self.cursor.execute("SELECT * FROM items ORDER BY bought ASC, name ASC")
        rows = self.cursor.fetchall()
        
        bought_count = 0
        for row in rows:
            status = "Да" if row[4] else "Нет"
            if row[4]: bought_count += 1
            self.tree.insert("", tk.END, iid=row[0], values=(row[1], row[2], row[3], status))
        
        self.lbl_stats.config(text=f"Всего: {len(rows)} | Куплено: {bought_count}")

    def add_item(self):
        name = self.ent_name.get().strip()
        qty_raw = self.spin_qty.get()
        cat = self.combo_cat.get()
        
        if not name:
            messagebox.showerror("Ошибка", "Введите название товара!")
            return

        try:
            qty = int(qty_raw)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть числом!")
            return
            
        self.cursor.execute("INSERT INTO items (name, qty, category) VALUES (?, ?, ?)", (name, qty, cat))
        self.conn.commit()
        
        
        self.ent_name.delete(0, tk.END)
        self.spin_qty.delete(0, tk.END)
        self.spin_qty.insert(0, "1")
        
        self.load_data()

    def toggle_bought(self):
        selected = self.tree.selection()
        if not selected: 
            return
        
        item_id = selected[0]
        self.cursor.execute("UPDATE items SET bought = CASE WHEN bought = 1 THEN 0 ELSE 1 END WHERE id = ?", (item_id,))
        self.conn.commit()
        self.load_data()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected: 
            return
        

        if messagebox.askyesno("Подтверждение", "Удалить выбранный товар?"):
            self.cursor.execute("DELETE FROM items WHERE id = ?", (selected[0],))
            self.conn.commit()
            self.load_data()

    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingListApp(root)
    root.mainloop()


#тест отправки ...