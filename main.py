import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime

conn = sqlite3.connect('access_records.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS access_log (
        AccessNum INTEGER PRIMARY KEY AUTOINCREMENT,
        ID INTEGER,
        Name TEXT,
        Access_Date DATETIME,
        Role TEXT
    )
''')
conn.commit()


def log_access():
    ID = id_entry.get()
    Name = name_entry.get()
    Role = role_var.get()
    access_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('INSERT INTO access_log (ID, Name, Access_Date, Role) VALUES (?, ?, ?, ?)',
                   (ID, Name, access_date, Role))
    conn.commit()
    status_label.config(text="Access logged successfully.")


def display_records():
    filter_by = filter_var.get()
    value = filter_value_entry.get()

    query = 'SELECT * FROM access_log'

    if filter_by and value:
        if filter_by == 'Date':
            query += f" WHERE date(Access_Date) = '{value}'"
        elif filter_by == 'ID':
            query += f" WHERE ID = {value}"
        elif filter_by == 'Time Range':
            start_time = start_time_entry.get()
            end_time = end_time_entry.get()
            query += f" WHERE Access_Date BETWEEN '{start_time}' AND '{end_time}'"

    cursor.execute(query)
    records = cursor.fetchall()

    if records:
        result_tree.delete(*result_tree.get_children())
        for record in records:
            result_tree.insert('', 'end', values=record)
    else:
        status_label.config(text="No records found.")


app = tk.Tk()
app.title("Access Tracking System")

input_frame = tk.Frame(app)
input_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

button_frame = tk.Frame(app)
button_frame.grid(row=0, column=1, padx=10, pady=10)

id_label = tk.Label(input_frame, text="ID (9 digit number):")
id_label.grid(row=0, column=0, sticky='e')
id_entry = tk.Entry(input_frame)
id_entry.grid(row=0, column=1)

name_label = tk.Label(input_frame, text="Name:")
name_label.grid(row=1, column=0, sticky='e')
name_entry = tk.Entry(input_frame)
name_entry.grid(row=1, column=1)

role_label = tk.Label(input_frame, text="Role:")
role_label.grid(row=2, column=0, sticky='e')
role_var = tk.StringVar()
role_combo = ttk.Combobox(input_frame, textvariable=role_var, values=["Student", "Faculty", "Staff", "Janitorial"])
role_combo.grid(row=2, column=1)

log_button = tk.Button(button_frame, text="Log Access", command=log_access)
log_button.pack(fill='x')

filter_label = tk.Label(app, text="Filter by:")
filter_label.grid(row=1, column=0, sticky='e')
filter_var = tk.StringVar()
filter_combo = ttk.Combobox(app, textvariable=filter_var, values=["Date", "ID", "Time Range"])
filter_combo.grid(row=1, column=1)

filter_value_label = tk.Label(app, text="Filter Value:")
filter_value_label.grid(row=2, column=0, sticky='e')
filter_value_entry = tk.Entry(app)
filter_value_entry.grid(row=2, column=1)

start_time_label = tk.Label(app, text="Start Time (YYYY-MM-DD HH:MM:SS):")
start_time_label.grid(row=3, column=0, sticky='e')
start_time_entry = tk.Entry(app)
start_time_entry.grid(row=3, column=1)

end_time_label = tk.Label(app, text="End Time (YYYY-MM-DD HH:MM:SS):")
end_time_label.grid(row=4, column=0, sticky='e')
end_time_entry = tk.Entry(app)
end_time_entry.grid(row=4, column=1)

display_button = tk.Button(app, text="Display Records", command=display_records)
display_button.grid(row=5, columnspan=2)

status_label = tk.Label(app, text="", fg="green")
status_label.grid(row=6, columnspan=2)

result_tree = ttk.Treeview(app, columns=("AccessNum", "ID", "Name", "Access Date", "Role"), show="headings")
result_tree.heading("AccessNum", text="Access Number")
result_tree.heading("ID", text="ID")
result_tree.heading("Name", text="Name")
result_tree.heading("Access Date", text="Access Date")
result_tree.heading("Role", text="Role")
result_tree.grid(row=7, column=0, columnspan=2)

app.mainloop()

conn.close()
