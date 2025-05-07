import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

# Initialize main window
root = tk.Tk()
root.title("Smart Student Task Manager")
root.geometry("800x500")

# Global task list
tasks = []

# Load tasks from file if exists
def load_tasks():
    global tasks
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            for task in tasks:
                insert_task_to_tree(task)

# Save tasks to file
def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

# Insert task into Treeview
def insert_task_to_tree(task):
    task_tree.insert("", "end", values=(task["title"], task["due_date"], task["priority"], task["status"]))

# Validate dd/mm/yyyy format
def is_valid_date(date_str):
    return re.match(r"^\d{2}/\d{2}/\d{4}$", date_str)

# Add new task
def add_task():
    title = title_entry.get()
    due_date = due_date_entry.get()
    priority = priority_var.get()

    if not title or not due_date or not priority:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    if not is_valid_date(due_date):
        messagebox.showerror("Date Error", "Due date must be in dd/mm/yyyy format.")
        return

    new_task = {"title": title, "due_date": due_date, "priority": priority, "status": "Pending"}
    tasks.append(new_task)
    insert_task_to_tree(new_task)
    save_tasks()
    clear_inputs()

# Clear input fields
def clear_inputs():
    title_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    priority_var.set("")

# Delete selected task
def delete_task():
    selected = task_tree.selection()
    if not selected:
        messagebox.showwarning("Select Task", "Please select a task to delete.")
        return

    index = task_tree.index(selected[0])
    task_tree.delete(selected[0])
    tasks.pop(index)
    save_tasks()

# Mark task as completed
def mark_completed():
    selected = task_tree.selection()
    if not selected:
        messagebox.showwarning("Select Task", "Please select a task to mark as completed.")
        return

    index = task_tree.index(selected[0])
    tasks[index]["status"] = "Completed"
    task_tree.item(selected[0], values=(tasks[index]["title"], tasks[index]["due_date"], tasks[index]["priority"], "Completed"))
    save_tasks()

# Edit selected task
def edit_task():
    selected = task_tree.selection()
    if not selected:
        messagebox.showwarning("Select Task", "Please select a task to edit.")
        return

    index = task_tree.index(selected[0])
    title = title_entry.get()
    due_date = due_date_entry.get()
    priority = priority_var.get()

    if not title or not due_date or not priority:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    if not is_valid_date(due_date):
        messagebox.showerror("Date Error", "Due date must be in dd/mm/yyyy format.")
        return

    tasks[index]["title"] = title
    tasks[index]["due_date"] = due_date
    tasks[index]["priority"] = priority

    task_tree.item(selected[0], values=(title, due_date, priority, tasks[index]["status"]))
    save_tasks()
    clear_inputs()

# ----- GUI Layout -----

# Input Fields
title_label = tk.Label(root, text="Task Title:")
title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, padx=10, pady=5)

due_date_label = tk.Label(root, text="Due Date (dd/mm/yyyy):")
due_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
due_date_entry = tk.Entry(root, width=40)
due_date_entry.grid(row=1, column=1, padx=10, pady=5)

priority_label = tk.Label(root, text="Priority:")
priority_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
priority_var = tk.StringVar()
priority_dropdown = ttk.Combobox(root, textvariable=priority_var, values=["High", "Medium", "Low"], width=37)
priority_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=3, column=0, padx=10, pady=10)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.grid(row=3, column=1, padx=100, pady=10, sticky="w")

complete_button = tk.Button(root, text="Mark Completed", command=mark_completed)
complete_button.grid(row=3, column=2, padx=10, pady=10)

# Task Table
task_tree = ttk.Treeview(root, columns=("Title", "Due Date", "Priority", "Status"), show="headings")
task_tree.heading("Title", text="Title")
task_tree.heading("Due Date", text="Due Date")
task_tree.heading("Priority", text="Priority")
task_tree.heading("Status", text="Status")
task_tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Load tasks on startup
load_tasks()

root.mainloop()
