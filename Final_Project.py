import tkinter as tk
from tkinter import messagebox
import os

FILENAME = "tasks.txt"
tasks = []


def load_tasks():
    global tasks
    tasks.clear()
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    description, priority, due_date, completed = parts
                    priority = int(priority) if priority else None
                    due_date = due_date if due_date else None
                    completed = completed == "True"
                    tasks.append({
                        "description": description,
                        "priority": priority,
                        "due_date": due_date,
                        "completed": completed
                    })


def save_tasks():
    with open(FILENAME, "w") as file:
        for task in tasks:
            file.write(f"{task['description']},{task['priority'] or ''},{task['due_date'] or ''},{task['completed']}\n")


def sort_tasks():
    return sorted(tasks, key=lambda t: (
        t["priority"] if t["priority"] is not None else float("inf"),
        t["due_date"] if t["due_date"] else "9999-99-99"
    ))


def view_tasks():
    listbox_tasks.delete(0, tk.END)
    sorted_list = sort_tasks()
    for idx, task in enumerate(sorted_list, 1):
        status = "✔ Completed" if task["completed"] else "✗ Pending"
        listbox_tasks.insert(
            tk.END,
            f"{idx}. {task['description']} | Priority: {task['priority']} | Due: {task['due_date']} | {status}"
        )


def add_task():
    desc = entry_desc.get().strip()
    priority = entry_priority.get().strip()
    due_date = entry_due.get().strip()
    if not desc:
        messagebox.showwarning("Warning", "Task description cannot be empty")
        return
    priority = int(priority) if priority.isdigit() else None
    due_date = due_date if due_date else None
    tasks.append({
        "description": desc,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    })
    save_tasks()
    view_tasks()
    entry_desc.delete(0, tk.END)
    entry_priority.delete(0, tk.END)
    entry_due.delete(0, tk.END)


def complete_task():
    selection = listbox_tasks.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Select a task to complete")
        return
    index = selection[0]
    sorted_list = sort_tasks()
    sorted_list[index]["completed"] = True
    tasks.clear()
    tasks.extend(sorted_list)
    save_tasks()
    view_tasks()


def remove_task():
    selection = listbox_tasks.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Select a task to remove")
        return
    index = selection[0]
    sorted_list = sort_tasks()
    tasks.remove(sorted_list[index])
    save_tasks()
    view_tasks()


def modify_priority():
    selection = listbox_tasks.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Select a task to modify priority")
        return
    new_priority = entry_priority.get().strip()
    if not new_priority.isdigit():
        messagebox.showwarning("Warning", "Priority must be a number")
        return
    index = selection[0]
    sorted_list = sort_tasks()
    sorted_list[index]["priority"] = int(new_priority)
    tasks.clear()
    tasks.extend(sorted_list)
    save_tasks()
    view_tasks()


def modify_due_date():
    selection = listbox_tasks.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Select a task to modify due date")
        return
    new_due = entry_due.get().strip()
    index = selection[0]
    sorted_list = sort_tasks()
    sorted_list[index]["due_date"] = new_due if new_due else None
    tasks.clear()
    tasks.extend(sorted_list)
    save_tasks()
    view_tasks()


window = tk.Tk()
window.title("Professional To-Do List Manager")
window.geometry("750x500")
window.config(bg="#f0f2f5")

title_label = tk.Label(window, text="To-Do List Manager", font=("Segoe UI", 18, "bold"), bg="#f0f2f5", fg="#333")
title_label.pack(pady=10)

frame_input = tk.Frame(window, bg="#ffffff", bd=1, relief="solid")
frame_input.pack(pady=10, padx=10, fill="x")

tk.Label(frame_input, text="Task Description:", font=("Segoe UI", 10), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_desc = tk.Entry(frame_input, width=50)
entry_desc.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Priority:", font=("Segoe UI", 10), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_priority = tk.Entry(frame_input, width=20)
entry_priority.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_input, text="Due Date (YYYY-MM-DD):", font=("Segoe UI", 10), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_due = tk.Entry(frame_input, width=20)
entry_due.grid(row=2, column=1, padx=5, pady=5, sticky="w")

frame_buttons = tk.Frame(window, bg="#f0f2f5")
frame_buttons.pack(pady=5)

btn_style = {
    "font": ("Segoe UI", 10),
    "width": 18,
    "bg": "#4a90e2",
    "fg": "white",
    "relief": "flat",
    "cursor": "hand2",
    "padx": 5,
    "pady": 5
}

tk.Button(frame_buttons, text="Add Task", command=add_task, **btn_style).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Complete Task", command=complete_task, **btn_style).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Remove Task", command=remove_task, **btn_style).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Modify Priority", command=modify_priority, **btn_style).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Modify Due Date", command=modify_due_date, **btn_style).grid(row=1, column=1, padx=5, pady=5)

listbox_tasks = tk.Listbox(window, width=100, height=15, font=("Consolas", 10))
listbox_tasks.pack(pady=10)

load_tasks()
view_tasks()

window.mainloop()
