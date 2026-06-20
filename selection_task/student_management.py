import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from datetime import datetime

# Install once: pip install reportlab
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DATA_FILE = "students.json"
students = []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

def load_data():
    global students
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            students = json.load(f)
    refresh_table()

def refresh_table(data=None):
    for item in tree.get_children():
        tree.delete(item)

    records = data if data is not None else students

    for s in records:
        tree.insert("", "end", values=(s["name"], s["age"], s["course"], s["email"]))

    total_label.config(text=f"Total Students: {len(records)}")

def clear_fields():
    name_var.set("")
    age_var.set("")
    course_var.set("")
    email_var.set("")

def add_student():
    if not all([name_var.get(), age_var.get(), course_var.get(), email_var.get()]):
        messagebox.showwarning("Warning", "Fill all fields")
        return

    students.append({
        "name": name_var.get(),
        "age": age_var.get(),
        "course": course_var.get(),
        "email": email_var.get()
    })

    save_data()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student Added Successfully")

def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a student")
        return

    values = tree.item(selected[0])["values"]

    for s in students:
        if (
            str(s["name"]) == str(values[0]) and
            str(s["age"]) == str(values[1]) and
            str(s["course"]) == str(values[2]) and
            str(s["email"]) == str(values[3])
        ):
            s["name"] = name_var.get()
            s["age"] = age_var.get()
            s["course"] = course_var.get()
            s["email"] = email_var.get()
            break

    save_data()
    refresh_table()
    clear_fields()

    messagebox.showinfo("Success", "Student Updated Successfully")


def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a student")
        return

    values = tree.item(selected[0])["values"]

    for s in students[:]:
        if (
            str(s["name"]) == str(values[0]) and
            str(s["age"]) == str(values[1]) and
            str(s["course"]) == str(values[2]) and
            str(s["email"]) == str(values[3])
        ):
            students.remove(s)
            break

    save_data()
    refresh_table()
    clear_fields()

    messagebox.showinfo("Success", "Student Deleted Successfully")


def select_row(event):
    selected = tree.selection()

    if selected:
        values = tree.item(selected[0])["values"]

        name_var.set(values[0])
        age_var.set(values[1])
        course_var.set(values[2])
        email_var.set(values[3])



def search_student():
    keyword = search_var.get().lower()
    result = [s for s in students if keyword in s["name"].lower()]
    refresh_table(result)

def filter_students():
    selected_course = filter_var.get()

    if not selected_course:
        refresh_table()
        return

    result = [s for s in students if s["course"] == selected_course]
    refresh_table(result)

def select_row(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])["values"]
        name_var.set(values[0])
        age_var.set(values[1])
        course_var.set(values[2])
        email_var.set(values[3])

def generate_report():
    # TXT REPORT
    with open("Student_Report.txt", "w") as f:
        f.write("NAYEPANKH FOUNDATION STUDENT REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now()}\n\n")

        for s in students:
            f.write(f"Name: {s['name']}\n")
            f.write(f"Age: {s['age']}\n")
            f.write(f"Course: {s['course']}\n")
            f.write(f"Email: {s['email']}\n")
            f.write("-" * 50 + "\n")

    # PDF REPORT
    pdf_file = "NayePankh_Student_Report.pdf"
    doc = SimpleDocTemplate(pdf_file)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("NayePankh Foundation Student Management Report", styles['Title']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 10))

    data = [["Name", "Age", "Course", "Email"]]

    for s in students:
        data.append([s["name"], s["age"], s["course"], s["email"]])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))

    elements.append(table)
    doc.build(elements)

    messagebox.showinfo("Success", "TXT and PDF Reports Generated")

root = tk.Tk()
root.title("NayePankh Foundation Student Management System")
root.geometry("1200x700")
root.configure(bg="#0F172A")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#1E293B",
                foreground="white",
                fieldbackground="#1E293B",
                rowheight=28)

style.configure("Treeview.Heading",
                background="#2563EB",
                foreground="white")

header = tk.Frame(root, bg="#1E293B")
header.pack(fill="x")

tk.Label(header,
         text="NayePankh Foundation Student Management System",
         bg="#1E293B",
         fg="white",
         font=("Segoe UI", 20, "bold")).pack(pady=15)

total_label = tk.Label(root,
                       text="Total Students: 0",
                       bg="#334155",
                       fg="white",
                       font=("Segoe UI", 12, "bold"))
total_label.pack(fill="x", padx=15, pady=10)

name_var = tk.StringVar()
age_var = tk.StringVar()
course_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()
filter_var = tk.StringVar()

form = tk.Frame(root, bg="#0F172A")
form.pack(fill="x", padx=15)

labels = [("Name", name_var), ("Age", age_var), ("Course", course_var), ("Email", email_var)]

for i, (txt, var) in enumerate(labels):
    tk.Label(form, text=txt, bg="#0F172A", fg="white").grid(row=i, column=0, padx=5, pady=5, sticky="w")
    tk.Entry(form, textvariable=var, width=40).grid(row=i, column=1)

btn = tk.Frame(form, bg="#0F172A")
btn.grid(row=0, column=2, rowspan=4, padx=20)

tk.Button(btn, text="Add", bg="#10B981", fg="white", width=15, command=add_student).pack(pady=3)
tk.Button(btn, text="Update", bg="#3B82F6", fg="white", width=15, command=update_student).pack(pady=3)
tk.Button(btn, text="Delete", bg="#EF4444", fg="white", width=15, command=delete_student).pack(pady=3)
tk.Button(btn, text="Generate Report", bg="#8B5CF6", fg="white", width=15, command=generate_report).pack(pady=3)

search_frame = tk.Frame(root, bg="#0F172A")
search_frame.pack(fill="x", padx=15, pady=10)

tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")
tk.Button(search_frame, text="Search", command=search_student).pack(side="left", padx=5)

ttk.Combobox(search_frame,
             textvariable=filter_var,
             values=["Python", "AI", "Web Development", "Data Science"],
             width=25).pack(side="left", padx=5)

tk.Button(search_frame, text="Filter", command=filter_students).pack(side="left")
tk.Button(search_frame, text="Show All", command=lambda: refresh_table()).pack(side="left", padx=5)

tree = ttk.Treeview(root, columns=("Name","Age","Course","Email"), show="headings")

for col in ("Name","Age","Course","Email"):
    tree.heading(col, text=col)
    tree.column(col, width=250)

tree.pack(fill="both", expand=True, padx=15, pady=10)
tree.bind("<<TreeviewSelect>>", select_row)

load_data()
root.mainloop()
