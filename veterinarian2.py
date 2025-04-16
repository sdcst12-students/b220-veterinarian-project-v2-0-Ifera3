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
        self.columData.update({'id':"INTEGER"})
        #print(self.columData)
        
    def createTable(self):
        query = f"create table if not exists {self.name} (id integer primary key autoincrement, {self.displayColumData()});"
        cursor.execute(query)
        cursor.execute(f'PRAGMA table_info({self.name});')
        return cursor.fetchall() # returns table info

class sqlData(sqlBase):
    def __init__(self, tableName, columsAndData, needToAdd = True):
        super().__init__(tableName, columsAndData)
        tablesInDatabase[self.tableName].entrys.append(self)
        if needToAdd:
            self.addEntry()
        #print(self.columData)
    
    def addEntry(self):
        query = f"insert into {self.tableName} ({self.colums}) Values ({self.displayData()});"
        cursor.execute(query)
        #cursor.execute(f'select * from {self.tableName};')
        #print(cursor.fetchall())

'''
query ="SELECT name FROM sqlite_master WHERE type='table';"
cursor.execute(query)
result = cursor.fetchall()
print(result)

for i in result:
    cursor.execute(f'PRAGMA table_info({i[0]});')
    print(cursor.fetchall(),i[0])
'''

def reAddTable():
    query = "SELECT * FROM sqlite_sequence;"
    cursor.execute(query)
    result = cursor.fetchall()
    #print(result)
    for table in result:
        #if table[0] == 'npc' or table[0] == 'customers':
        #    continue
        columnType = {}
        cursor.execute(f'PRAGMA table_info({table[0]});')
        columns = cursor.fetchall()
        for column in columns:
            columnType.update({column[1]:column[2]})
        sqlTable(table[0],columnType)
        
reAddTable()

#sqlTable("Test", {'name':'tinytext'})
#sqlTable("Test2", {"name":"tinytext","number":"integer"})
#sqlData("Test2", {"name":"Joe",'number':3})
#print(tablesInDatabase['Test2'].entrys)

def surchTable(surchTable, surchColum, surchData, requestedData = "*"):
    if surchTable not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if surchColum not in tablesInDatabase[surchTable].columData: # if the requested colum does not exsist won't crash 
        return None
    query = f"Select {requestedData} from {tablesInDatabase[surchTable].name} where {surchColum} = {surchData};"
    cursor.execute(query)
    return cursor.fetchall()

#print(surchTable("Test2","name", "'Joe'"))
#connection.commit()

def changeEntry(table, id, updateColum, updateData):
    if table not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if updateData not in tablesInDatabase[surchTable].columData: # if the requested colum does not exsist won't crash  
        return None
    query = f"Update {tablesInDatabase[table].name} set {updateColum} = {updateData} where id = {id};"
    cursor.execute(query)
    return cursor.fetchall()


window = tk.Tk()
window.attributes('-topmost',True)

'''
fromBox = tk.StringVar()
box = tk.Entry(window,textvariable=fromBox)
box.grid(row=1,column=1,padx=10,pady=10)
def show():
    print(fromBox.get())
push = tk.Button(window,text="Enter",command=show)
push.grid(row=1,column=2)
'''

instructionsText = tk.StringVar(window,'Test')
instructionsLable = tk.Label(window,textvariable=instructionsText)
instructionsLable.grid(row=1,column=1,columnspan=10,padx=10)
tempButon = []
tempRadio = []
tempLable = []
tempEnter = []

def clearWindow():
    global tempButon, tempRadio, tempLable, tempEnter
    instructionsText.set('')
    for buton in tempButon:
        buton.destroy()
    for radio in tempRadio:
        radio.destroy()
    for lable in tempLable:
        lable.destroy()
    tempButon = []
    tempRadio = []
    tempLable = []
    tempEnter = []

def continueOption(optionSelected): #return what table is selected
    clearWindow()
    if optionSelected == "surch":
        tempEnter.insert(0,tk.Entry(window))
        tempEnter[0].grid(row=3,column=1,pady=10,padx=10)

def tableSelect(option): #return what table is selected
    global tableSelected
    instructionsText.set("Select Table")
    tableSelected = tk.StringVar(window)
    a = 0
    tempLable.append(tk.Label(window,text='You have Selected:'))
    tempLable[-1].grid(row=3,column=1)
    tempLable.append(tk.Label(window,textvariable=tableSelected))
    tempLable[-1].grid(row=3,column=2)
    for table in tablesInDatabase:
        tempRadio.append(tk.Radiobutton(window,variable=tableSelected,value=table,text=table))
        tempRadio[a].grid(row=2,column=1+a,padx=10,pady=10)
        tableSelected.set(table)
        a += 1
    tempButon.append(tk.Button(window,text='Submit',command=lambda:continueOption(option)))
    tempButon[-1].grid(row=3,column=3)
    
    

def startoption(option):
    stopOptionSelect()
    tableSelect(option)

def startEdit():
    ...

surchButton = tk.Button(window,text='Surch Table',command=lambda:startoption('surch'))
editButton = tk.Button(window,text='Edit Entry',command=lambda:startoption('edit'))

def stopOptionSelect():
    surchButton.grid_forget()
    editButton.grid_forget()

def startOptionSelect():
    instructionsText.set("Select Option")
    surchButton.grid(column=1,row=2,padx=10,pady=10)
    editButton.grid(column=2,row=2,padx=10,pady=10)

startOptionSelect()

'''
def adding():
    #tempText = []
    b = 1
    e = 0
    for table in tablesInDatabase:
        a = 0
        for i in tablesInDatabase[table].columData:
            tempButon.append(tk.Button(window,text=i))
            tempButon[e].grid(row=b,column=a,padx=10,pady=10)
            a += 1
            e += 1
        b += 1

add = tk.Button(window,text='add',command=adding)
add.grid(row=10,column=10,padx=10,pady=10)

def removing():
    global tempButon
    for button in tempButon:
        button.destroy()
    tempButon = []

remove = tk.Button(window,text='remove',command=removing)
remove.grid(row=10,column=9,padx=10,pady=10)
'''
""" first test of temperary buttons
tempButon = []
tempText = []
b = 1
e = 0
for table in tablesInDatabase:
    a = 0
    for i in tablesInDatabase[table].columData:
        tempButon.append(tk.Button(window,text=i))
        tempButon[e].grid(row=b,column=a,padx=10,pady=10)
        a += 1
        e += 1
    b += 1
"""
window.mainloop()
