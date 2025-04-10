#Python 3

import tkinter as tk
import sqlite3

connection = sqlite3.connect("dbase.db")
cursor = connection.cursor()

tablesInDatabase = {}

class sqlBase(): # parent class for all sql objects
    def __init__(self, tableName, columsAndData, name = None):
        self.name = name
        self.tableName = tableName
        self.columData = columsAndData
        self.colums = ''
        for colum in self.columData:
            self.colums += ', ' + colum
        else:
            self.colums = self.colums.replace(', ','',1)
        #print(self.colums)
    
    def displayColumData(self, mid = '',  colums = ''):
        for colum in self.columData:
            colums += f", {colum} {mid} {self.columData[colum]}"
        colums = colums.replace(', ','',1)
        return colums

    def displayData(self, colums = ''):
        for colum in self.columData:
            if tablesInDatabase[self.tableName].columData[colum] == 'tinytext':
                colums += f", '{self.columData[colum]}'"
            else:
                colums += f", {self.columData[colum]}"
        colums = colums.replace(', ','',1)
        return colums

    def __str__(self):
        ...


class sqlTable(sqlBase):
    def __init__(self, tableName, columsAndDataType, vishualName = None):
        self.entrys = []
        if vishualName == None:
            super().__init__(tableName,columsAndDataType,tableName)
        else:
            super().__init__(tableName,columsAndDataType,vishualName)
        result = self.createTable()
        #print(result)
        tablesInDatabase.update({self.name:self})
        query = f"select * from {self.tableName};"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            data = {}
            for column in range(1,len(row)):
               data.update({result[column][1]:row[column]})
            #print(data)
            sqlData(self.tableName,data,False)
        
    def createTable(self):
        query = f"create table if not exists {self.name} (id integer primary key autoincrement, {self.displayColumData()});"
        cursor.execute(query)
        cursor.execute(f'PRAGMA table_info({self.name});')
        return cursor.fetchall() # returns table info

class sqlData(sqlBase):
    def __init__(self, tableName, columsAndData,needToAdd = True):
        super().__init__(tableName, columsAndData)
        tablesInDatabase[self.tableName].entrys.append(self)
        if needToAdd:
            self.addEntry()
    
    def addEntry(self):
        query = f"insert into {self.tableName} ({self.colums}) Values ({self.displayData()});"
        cursor.execute(query)
        #cursor.execute(f'select * from {self.tableName};')
        #print(cursor.fetchall())


#sqlTable("Test", {'name':'tinytext'})
sqlTable("Test2", {"name":"tinytext","number":"integer"})
#sqlData("Test2", {"name":"Joe",'number':3})
print(tablesInDatabase['Test2'].entrys[0].columData)

def surchTable(surchTable, surchColum, surchData, requestedData = "*"):
    if surchTable not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if surchColum not in tablesInDatabase[surchTable].columData and surchColum != 'id': # if the requested colum does not exsist won't crash 
        return None
    query = f"Select {requestedData} from {tablesInDatabase[surchTable].name} where {surchColum} = {surchData};"
    cursor.execute(query)
    return cursor.fetchall()

print(surchTable("Test2","name", "'Joe'"))
#connection.commit()

def changeEntry(table, id, updateColum, updateData):
    if table not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if updateData not in tablesInDatabase[surchTable].columData and updateColum != 'id': # if the requested colum does not exsist won't crash  
        return None
    query = f"Update {tablesInDatabase[table].name} set {updateColum} = {updateData} where id = {id};"
    cursor.execute(query)
    return cursor.fetchall()

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