#Python 3

import tkinter as tk
import sqlite3

connection = sqlite3.connect("dbase.db")
cursor = connection.cursor()

tablesInDatabase = {}

class sqlBase():
    def __init__(self, tableName, columsAndData, name = None):
        self.name = name
        self.tableName = tableName
        self.colums = columsAndData
    
    def __str__(self):
        ...

class table(sqlBase):
    def __init__(self, tableName, columsAndDataType, vishualName = None):
        self.entrys = []
        if vishualName == None:
            super().__init__(tableName,columsAndDataType,tableName)
        else:
            super().__init__(tableName,columsAndDataType,vishualName)
        self.columString = "id integer primary key autoincrement"
        for colum in columsAndDataType:
            self.columString += ", " + colum
        result = self.createTable()
        #print(result)
        tablesInDatabase[vishualName] = self
        
    def createTable(self):
        colums = ''
        for colum in self.colums:
            colums += f", {colum} {self.colums[colum]}"
        query = f"create table if not exists {self.name} (id integer primary key autoincrement{colums});"
        cursor.execute(query)
        cursor.execute(f'PRAGMA table_info({self.name});')
        return cursor.fetchall()

class sqlData(sqlBase):
    def __init__(self, tableName, columsAndData):
        super().__init__(tableName, columsAndData)
        self.addEntry()
    
    def addEntry(self):
        ...


table("Test", {'name':'tinytext'})
table("Test2", {"name":"tinytext","number":"integer"})
print(tablesInDatabase['Test2'].colums)

def surchTable(surchTable, surchColum, surchData, requestedData = "*"):
    if surchColum not in tablesInDatabase[surchTable].colums:
        return False, None
    query = f"Select {requestedData} from {tablesInDatabase[surchTable].name} where {surchColum} = {surchData};"
    cursor.execute(query)
    return True, cursor.fetchall()

def addEntery(table, newDataObject):
    query = f"insert into {table.name} ({table.columString}) values ({newDataObject});"
    cursor.execute(query)

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