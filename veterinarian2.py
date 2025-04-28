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
    print(surchTable, surchColum, surchData, requestedData)
    if surchTable not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if surchColum not in tablesInDatabase[surchTable].columData: # if the requested colum does not exsist won't crash 
        return None
    query = f"Select {requestedData} from {tablesInDatabase[surchTable].name} where {surchColum} = {surchData};"
    print(query)
    cursor.execute(query)
    #print(cursor.fetchall())
    return cursor.fetchall()

#print(surchTable("Test2","name", "'Joe'"))
#connection.commit()

def changeEntry(table, id, updateColum, updateData):
    if table not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if updateColum not in tablesInDatabase[table].columData: # if the requested colum does not exsist won't crash  
        return None
    query = f"Update {tablesInDatabase[table].name} set {updateColum} = {updateData} where id = {id};"
    print(query)
    cursor.execute(query)
    tablesInDatabase[table].entrys[id-1].columData[updateColum]=updateData
    #connection.commit()
    return None #cursor.fetchall()


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
    for enter in tempEnter:
        enter.destroy()
    tempButon = []
    tempRadio = []
    tempLable = []
    tempEnter = []

def continueOption(optionSelected,tableSelected): #return what table is selected
    clearWindow()
    if optionSelected == "surch":
        colum = tk.StringVar(window)
        a=1
        for column in tablesInDatabase[tableSelected].columData:
            tempRadio.append(tk.Radiobutton(window,variable=colum,value=column,text=column))
            tempRadio[-1].grid(row=2,column=a,padx=10,pady=10)
            a+=1
        colum.set('id')
        tempButon.append(tk.Button(window,text="Submit",command=lambda:continueSurchData(tableSelected,[colum.get()])))
        tempButon[-1].grid(row=3,column=1,padx=10,pady=10)
    if optionSelected == "edit":
        instructionsText.set("Enter the ID you would like to edit")
        tempEnter.append(tk.Entry(window))
        tempEnter[0].grid(row=2,column=1,pady=10,padx=10)
        tempButon.append(tk.Button(window,text="Submit",command=lambda:continueEditColum(tableSelected,tempEnter[0].get())))
        tempButon[-1].grid(row=3,column=1,padx=10,pady=10)

def continueEditColum(table,editID):
    clearWindow()
    colum = tk.StringVar(window)
    instructionsText.set("Select column of the data you want to change")
    a=1
    for column in tablesInDatabase[table].columData:
        tempRadio.append(tk.Radiobutton(window,variable=colum,value=column,text=column))
        tempRadio[-1].grid(row=2,column=a,padx=10,pady=10)
        a+=1
    colum.set('id')
    tempButon.append(tk.Button(window,text="Submit",command=lambda:continueEditData(table,editID,colum.get())))
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)

def continueEditData(table,editID,editColumn):
    clearWindow()
    instructionsText.set("Enter the data you would like have")
    tempEnter.append(tk.Entry(window))
    tempEnter[0].grid(row=2,column=1,pady=10,padx=10)
    tempButon.append(tk.Button(window,text="Submit",command=lambda:editColum(table,editID,editColumn,tempEnter[0].get())))
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)

def continueSurchData(tableSelected,surchData):
    clearWindow()
    tempEnter.insert(0,tk.Entry(window))
    tempEnter[0].grid(row=2,column=1,pady=10,padx=10)
    tempButon.append(tk.Button(window,text="Submit",command=lambda:continueSurchFindNum(tableSelected,surchData,tempEnter[0].get())))
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)

def continueSurchFindNum(tableSelected,surchData,data):
    clearWindow()
    if tablesInDatabase[tableSelected].columData[surchData[0]] == 'tinytext':
        data = f"'{data}'"
    surchData.append(data)
    #print(surchData)
    chose = tk.IntVar(window)
    a=1
    for num in range(len(tablesInDatabase[tableSelected].columData)):
        if num == len(tablesInDatabase[tableSelected].columData)-1:
            tempRadio.append(tk.Radiobutton(window,variable=chose,value=num+1,text='All'))
            tempRadio[-1].grid(row=4,column=a,padx=10,pady=10)
        else:
            tempRadio.append(tk.Radiobutton(window,variable=chose,value=num+1,text=num+1))
            tempRadio[-1].grid(row=4,column=a,padx=10,pady=10)
        a+=1
    tempButon.append(tk.Button(window,text='Submit',command=lambda:continueSurchFindColum(tableSelected,surchData,chose.get(),0,[])))
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)


def continueSurchFindColum(tableSelected,surchData,num,loopNum,findColums,add=None):
    clearWindow()
    if add != None:
        findColums.append(add)
    if num == len(tablesInDatabase[tableSelected].columData):
        startSurch(tableSelected,surchData[0],surchData[1],'*')
    elif loopNum == num:
        startSurch(tableSelected,surchData[0],surchData[1],findColums)
    else:
        colum = tk.StringVar(window)
        a=1
        for column in tablesInDatabase[tableSelected].columData:
            if column in findColums:
                continue
            tempRadio.append(tk.Radiobutton(window,variable=colum,value=column,text=column))
            tempRadio[-1].grid(row=2,column=a,padx=10,pady=10)
            a+=1
        colum.set('id')
        tempButon.append(tk.Button(window,text='Submit',command=lambda:continueSurchFindColum(tableSelected,surchData,num,loopNum+1,findColums,colum.get())))
        tempButon[-1].grid(row=3,column=1,padx=10,pady=10)


'''tempEnter.insert(1,tk.Entry(window))
tempEnter[1].grid(row=3,column=2,pady=10,padx=10)
tempEnter.insert(2,tk.Entry(window))
tempEnter[2].grid(row=3,column=3,pady=10,padx=10)'''
#tempButon.insert(0,tk.Button(window,text="surch",command=lambda:startSurch(tableSelected,colum.get(),tempEnter[0].get(),tempEnter[2].get())))
#tempButon[0].grid(row=3,column=4,pady=10,padx=10)

def editColum(table,editID,editcolumn,editData):
    clearWindow()
    if tablesInDatabase[table].columData[editcolumn] == "tinytext":
        editData = f"'{editData}'"
    changeEntry(table,editID,editcolumn,editData)
    entery = surchTable(table,editcolumn,editData)
    instructionsText.set(entery[0])
    tempButon.append(tk.Button(window,text='Menu',command=startOptionSelect))
    tempButon[-1].grid(row=2,column=1)

def startSurch(table, colum, data, findlist):
    clearWindow()
    find = ', '.join(findlist)
    result = surchTable(table,colum,data,find)
    #print(result,table, colum, data, find)
    if result == []:
        tempLable.append(tk.Label(window,text=f"No {data} was found in column {colum} of table {table}"))
        tempLable[-1].grid(row=3,column=1,pady=10,padx=10)
    else:
        for i in range(len(result)):
            tempLable.append(tk.Label(window,text=result[i]))
            tempLable[-1].grid(row=3+i,column=1,pady=3,padx=10)
    tempButon.append(tk.Button(window,text='Menu',command=startOptionSelect))
    tempButon[-1].grid(row=2,column=1)

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
    tempButon.append(tk.Button(window,text='Submit',command=lambda:continueOption(option,tableSelected.get())))
    tempButon[-1].grid(row=3,column=3) 
    

def startoption(option):
    surchButton.grid_forget()
    editButton.grid_forget()
    tableSelect(option)

surchButton = tk.Button(window,text='Surch Table',command=lambda:startoption('surch'))
editButton = tk.Button(window,text='Edit Entry',command=lambda:startoption('edit'))

def startOptionSelect():
    clearWindow()
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
