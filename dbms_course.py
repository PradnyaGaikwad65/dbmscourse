from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
import sqlite3 

window = Tk()
window.title("courses")
window.geometry("1200x750")
window.configure(bg="#ADD8E6")

def save():
    S_id = student_id.get()
    Stu_name = student_name.get()
    Faculty = faculty_name.get()
    Course = course.get()
    Marks = marks.get()

    conn = sqlite3.connect('studata.db')
    cursor = conn.cursor()

    table_create = '''CREATE TABLE IF NOT EXISTS Stu_data(StuID INTEGER PRIMARY KEY, StudentName TEXT, Faculty TEXT, Course TEXT, Marks INT)'''
    cursor.execute(table_create)

    cursor.execute('''INSERT INTO Stu_data (StuID, StudentName, Faculty, Course, Marks) VALUES (?, ?, ?, ?, ?)''',
                   (S_id, Stu_name, Faculty,  Course, Marks))
    conn.commit()
    conn.close()

    clear_fields()

def search():
    def searchrecord():
        search_id = SID.get()
        
        conn = sqlite3.connect('studata.db')
        cursor = conn.cursor()

        if search_id:
            cursor.execute('''SELECT * FROM Stu_data WHERE StuID=?''', (search_id))
            search_results = cursor.fetchall()
            if search_results:
                display_search_results(search_results)
            else:
                display_label.config(text="Not found.")
        
        conn.close()

    addroot = Toplevel(master=window)
    addroot.grab_set()
    addroot.geometry("850x300")
    addroot.title("Search record")
    addroot.config(bg="#ADD8E6")

    tk.Label(addroot, text="Search by StudentID ", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")

    tk.Label(addroot, text="Enter StudentID:", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")
    SID = tk.Entry(addroot, bg="#ADD8E6")
    SID.pack(anchor="w", padx=30)

    display_label = tk.Label(addroot, text="", bg="#ADD8E6", font=font_style)
    display_label.pack()

    btn = tk.Button(addroot, text="Search", bg="#ADD8E6", command=searchrecord)
    btn.pack(side=LEFT, padx=30)

def delete():
    def deleterecord():
        S_id = SID.get()

        conn = sqlite3.connect('studata.db')
        cursor = conn.cursor()

        cursor.execute('''DELETE FROM Stu_data WHERE StuID=?''', (S_id,))
        popup=Toplevel(master=addroot)
        popup.grab_set()
        popup.geometry("300x100")
        popup.config(bg="#ADD8E6")
        tk.Label(popup, text="Record successfully deleted", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="center")

        conn.commit()
        conn.close()
        
        addroot.destroy()
        
    addroot = Toplevel(master=window)
    addroot.grab_set()
    addroot.geometry("550x250")
    addroot.title("Delete record")
    addroot.config(bg="#ADD8E6")

    tk.Label(addroot, text="Delete by Student ID", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")

    tk.Label(addroot, text="Enter Student ID:", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")
    SID = tk.Entry(addroot, bg="#ADD8E6")
    SID.pack(anchor="w", padx=30)

    btn = tk.Button(addroot, text="Delete", bg="#ADD8E6", command=deleterecord)
    btn.pack(side=LEFT, padx=30)

def clear_fields():
    stu_id.delete(0, END)
    stu_name.delete(0, END)
    faculty_name.delete(0, END)
    course.delete(0, END)
    marks.delete(0, END)

def display_search_results(results):
    addroot= Toplevel(master=window)
    addroot.geometry("800x500")
    treeview = ttk.Treeview(addroot)
    treeview.pack()

    treeview["columns"] = ("StudentID", "StudentName", "Faculty", "Course", "Marks")

    treeview.column("#0", width=0, stretch=NO)
    treeview.column("StudentID", anchor=E, width=70)
    treeview.column("StudentName", anchor=E, width=100)
    treeview.column("Faculty", anchor=E, width=70)
    treeview.column("Course", anchor=E, width=70)
    treeview.column("Marks", anchor=E, width=70)

    treeview.heading("#0", text="", anchor=W)
    treeview.heading("StudentID", text="StudentID", anchor=W)
    treeview.heading("StudentName", text="StudentName", anchor=W)
    treeview.heading("Faculty", text="Faculty", anchor=W)
    treeview.heading("Course", text="Course", anchor=W)
    treeview.heading("Marks", text="Marks", anchor=W)

    for row in results:
        treeview.insert("", END, values=row)

def display():
    conn= sqlite3.connect('studata.db')
    cursor= conn.cursor()

    display_window= Toplevel(master=window)
    display_window.title("Display Data")
    display_window.geometry("900x550")

    treeview= ttk.Treeview(display_window)
    treeview.pack()

    treeview["columns"] = ("StuID", "StudentName", "Faculty",  "Course", "Marks")

    cursor.execute("SELECT * from Stu_data")
    data= cursor.fetchall()

    conn.commit()
    conn.close()

    for row in data:
        treeview.insert("", END, values=row)

    treeview.column("#0", width=0, stretch=NO)
    treeview.column("StuID", anchor=CENTER, width=80)
    treeview.column("StudentName", anchor=CENTER, width=120)
    treeview.column("Faculty", anchor=CENTER, width=100)
    treeview.column("Course", anchor=CENTER, width=100)
    treeview.column("Marks", anchor=CENTER, width=80)

    treeview.heading("#0", text="", anchor=W)
    treeview.heading("StuID", text="StudentID", anchor=CENTER)
    treeview.heading("StudentName", text="StudentName", anchor=CENTER)
    treeview.heading("Faculty", text="Faculty", anchor=CENTER)
    treeview.heading("Course", text="Course", anchor=CENTER)
    treeview.heading("Marks", text="Marks", anchor=CENTER)

font_style = ("Times New Roman", 20)
font_style1 = ("Times New Roman", 24)

Label(window, text="Course Database", font=font_style1, bg="#ADD8E6").pack()

frame = Frame(window, bg="#ADD8E6")
frame.pack(anchor="nw", pady=20)

btn = Button(frame, text="Save", bg="#ADD8E6", command=save)
btn.pack(side=LEFT, padx=30)

btn_search = Button(frame, text="Search", bg="#ADD8E6", command=search)
btn_search.pack(side=LEFT, padx=30)

btn_delete = Button(frame, text="Delete", bg="#ADD8E6", command=delete)
btn_delete.pack(side=LEFT, padx=30)

btn_display= Button(frame, text="Display", bg="#ADD8E6", command=display)
btn_display.pack(side=LEFT, padx=30)

Label(window, text="StudentID:", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")
student_id = Entry(window, bg="#ADD8E6")
student_id.pack(anchor="w", padx=30)

Label(window, text="StudentName:", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")
student_name = Entry(window, bg="#ADD8E6")
student_name.pack(anchor="w", padx=30)

Label(window, text="FacultyName:", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")
faculty_name = Entry(window, bg="#ADD8E6")
faculty_name.pack(anchor="w", padx=30)

Label(window, text="Course:", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")
course = Entry(window, bg="#ADD8E6")
course.pack(anchor="w", padx=30)

Label(window, text="Marks:", bg="#ADD8E6", font=font_style, padx=30).pack(anchor="w")
marks = Entry(window, bg="#ADD8E6")
marks.pack(anchor="w", padx=30)

display_label = Label(window, text="", bg="#ADD8E6", font=font_style)
display_label.pack()

window.mainloop()