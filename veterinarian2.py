#Python 3

import tkinter as tk
import sqlite3

connection = sqlite3.connect("dbase.db")
cursor = connection.cursor()

def createTable(tableName, tableColums):
    colums = ''
    if len(tableColums) == 1000:
        colums = ''
    else:
        for colum in tableColums:
            colums += f", {colum} {tableColums[colum]}"
    query = f"create table if not exists {tableName} (id integer primary key autoincrement{colums});"
    cursor.execute(query)
    cursor.execute(f'PRAGMA table_info({tableName});')
    print(cursor.fetchall())

createTable("Test2", {"name":"tinytext","number":"integer"})

def surchTable():
    ...

def addEntery():
    ...

def changeEntry():
    ...

"""
window = tk.Tk()
window.attributes('-topmost',True)

fromBox = tk.StringVar()

box = tk.Entry(window,textvariable=fromBox)
box.grid(row=1,column=1,padx=10,pady=10)

def show():
    print(fromBox.get())

push = tk.Button(window,text="Enter",command=show)
push.grid(row=1,column=2)

window.mainloop()
"""