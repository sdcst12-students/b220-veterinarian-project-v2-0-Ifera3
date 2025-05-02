#Python 3

import tkinter as tk
import sqlite3

#conects to data base
connection = sqlite3.connect("dbase.db")
cursor = connection.cursor()
tablesInDatabase = {}

class sqlBase(): # parent class for all sql objects
    def __init__(self, tableName, columsAndData, name = None): # Base __init__() for all sql classes
        self.name = name
        self.tableName = tableName
        self.columData = columsAndData
        self.colums = ''
        for colum in self.columData:
            self.colums += ', ' + colum
        else:
            self.colums = self.colums.replace(', ','',1)
        #print(self.colums)
    
    def displayColumData(self, mid = '',  colums = ''):#disblaeis each column and their data for print
        for colum in self.columData:
            colums += f", {colum} {mid} {self.columData[colum]}"
        colums = colums.replace(', ','',1)
        return colums

    def displayData(self, colums = ''):#disblaeis each column and their data for sqlite3
        for colum in self.columData:
            if tablesInDatabase[self.tableName].columData[colum] == 'tinytext' or tablesInDatabase[self.tableName].columData[colum] == 'mediumtext': # string are given '' to be read by sqlite as a string
                colums += f", '{self.columData[colum]}'"
            else:
                colums += f", {self.columData[colum]}"
        colums = colums.replace(', ','',1)
        return colums

    def __str__(self): # prints all columns and data
        return self.displayColumData(self)


class sqlTable(sqlBase): # sql table object with sql parent class
    def __init__(self, tableName, columsAndDataType, vishualName = None):
        self.entrys = []
        if vishualName == None:#if no visual name adds table name as visual name
            super().__init__(tableName,columsAndDataType,tableName)#sql parent object __init__()
        else:
            super().__init__(tableName,columsAndDataType,vishualName)#sql parent object __init__()
        result = self.createTable()
        #print(result)
        tablesInDatabase.update({self.name:self}) #adds itself to tables dictionary
        query = f"select * from {self.tableName};" #Finds enries in table to be added as objects
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            data = {}
            for column in range(1,len(row)):#finds all info in a table entry
               data.update({result[column][1]:row[column]})
            #print(data)
            sqlData(self.tableName,data,False)
        self.columData.update({'id':"INTEGER"})#adds id to columns as not returned when adding
        #print(self.columData)
        
    def createTable(self):#creates a sqlite3 table in the data base file if it does not exist
        query = f"create table if not exists {self.name} (id integer primary key autoincrement, {self.displayColumData()});"
        #print(query)
        cursor.execute(query)
        connection.commit()
        cursor.execute(f'PRAGMA table_info({self.name});')
        return cursor.fetchall() # returns table info

class sqlData(sqlBase):#object for table entreis, has parent sql object
    def __init__(self, tableName, columsAndData, needToAdd = True):
        super().__init__(tableName, columsAndData)#sql parent object __init__()
        tablesInDatabase[self.tableName].entrys.append(self)
        if needToAdd:
            self.addEntry()
        #print(self.columData)
    
    def addEntry(self):
        query = f"insert into {self.tableName} ({self.colums}) Values ({self.displayData()});"
        cursor.execute(query)
        connection.commit()
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

def reAddTable():#finds all tables in data base and adds them to the dictionary od table with their name and object
    query = "SELECT * FROM sqlite_sequence;"
    cursor.execute(query)
    result = cursor.fetchall()
    #print(result)
    for table in result:
        if table[0] == 'npc' or table[0] == 'customers' or table[0] == 'Test2':#test tables that are not in the final project
            continue
        columnType = {}
        cursor.execute(f'PRAGMA table_info({table[0]});')
        columns = cursor.fetchall()
        for column in columns:
            columnType.update({column[1]:column[2]})
        sqlTable(table[0],columnType)
        

#sqlTable("owners",{'firstName':'tinytext','lastName':'tinytext','phoneNum':'tinyint','email':'tinytext','adress':'tinytext','city':'tinytext','postalcode':'tinytext'})
#sqlTable("pets",{'name':'tinytext','type':'tinytext','breed':'tinytext','birthdate':'tinytext','ownerID':'integer'})
#sqlTable("visits",{'ownerID':'integer','petID':'integer','details':'mediumtext','cost':'integer','paid':'integer'})
#sqlTable("Test", {'name':'tinytext'})
#sqlTable("Test2", {"name":"tinytext","number":"integer"})
#sqlData("Test2", {"name":"Joe",'number':3})
#print(tablesInDatabase['Test2'].entrys)

def surchTable(surchTable, surchColum, surchData, requestedData = "*"):#Finds a entery in a table, needs table name, column that data is in, the known data, columns to be returned with a defult of returning all
    #print(surchTable, surchColum, surchData, requestedData)
    if surchTable not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if surchColum not in tablesInDatabase[surchTable].columData: # if the requested colum does not exsist won't crash 
        return None
    query = f"Select {requestedData} from {tablesInDatabase[surchTable].name} where {surchColum} = {surchData};"
    #print(query)
    cursor.execute(query)
    #print(cursor.fetchall())
    return cursor.fetchall()

#print(surchTable("Test2","name", "'Joe'"))
#connection.commit()

def changeEntry(table, id, updateColum, updateData):#Changes table entry, needs the table name, id of entry, column of data to be changed and the new data
    if table not in tablesInDatabase:# If table does not exsist stop from crash
        return None
    if updateColum not in tablesInDatabase[table].columData: # if the requested colum does not exsist won't crash  
        return None
    query = f"Update {tablesInDatabase[table].name} set {updateColum} = {updateData} where id = {id};"
    #print(query)
    cursor.execute(query)
    tablesInDatabase[table].entrys[id-1].columData[updateColum]=updateData
    connection.commit()
    return None #cursor.fetchall()

window = tk.Tk()
window.attributes('-topmost',True)

#lable that is always present to give instructions
instructionsText = tk.StringVar(window,'Test')
instructionsLable = tk.Label(window,textvariable=instructionsText)
instructionsLable.grid(row=1,column=1,columnspan=10,padx=10)
#lists for window elements that are tempurary and will cange
tempButon = []
tempRadio = []
tempLable = []
tempEnter = []

def clearWindow():#clears all elements on the window except the main elimints
    global tempButon, tempRadio, tempLable, tempEnter
    instructionsText.set('')
    #removes all eliments
    for buton in tempButon:
        buton.destroy()
    for radio in tempRadio:
        radio.destroy()
    for lable in tempLable:
        lable.destroy()
    for enter in tempEnter:
        enter.destroy()
    #clears all lists
    tempButon = []
    tempRadio = []
    tempLable = []
    tempEnter = []

def continueOption(optionSelected,tableSelected): #splits into each selected option
    clearWindow()
    if optionSelected == "surch":
        #Next function is continueSurchData() line 260
        instructionsText.set("Select the column that you are surching in")
        colum = tk.StringVar(window) # user select column that the data they are looking for is in
        a=1
        for column in tablesInDatabase[tableSelected].columData: # iterates through alln columns in selected table and creats radio buttons to select column
            tempRadio.append(tk.Radiobutton(window,variable=colum,value=column,text=column))
            tempRadio[-1].grid(row=2,column=a,padx=10,pady=10)
            a+=1
        colum.set('id') # selects id by defult
        tempButon.append(tk.Button(window,text="Submit",command=lambda:continueSurchData(tableSelected,[colum.get()]))) #Button to Submit selection and move to next step
        tempButon[-1].grid(row=3,column=1,padx=10,pady=10)
    if optionSelected == "edit":
        #Next function is continueEditColum() line 239
        instructionsText.set("Enter the ID you would like to edit")
        tempEnter.append(tk.Entry(window)) # gets id of entry to edit
        tempEnter[0].grid(row=2,column=1,pady=10,padx=10)
        tempButon.append(tk.Button(window,text="Submit",command=lambda:continueEditColum(tableSelected,tempEnter[0].get()))) #Button to Submit selection and move to next step
        tempButon[-1].grid(row=3,column=1,padx=10,pady=10)
    if optionSelected == "create":
        #Next function is addEntry() line 222
        instructionsText.set("Enter the data for the new entery")
        columns = []
        entrys = 1
        for columnlable in tablesInDatabase[tableSelected].columData: # add a lable for each column in the selected table
            if columnlable == 'id':
                continue
            tempLable.append(tk.Label(window,text=columnlable))
            tempLable[-1].grid(row=2,column=entrys,padx=10,pady=10)
            columns.append(columnlable)
            entrys +=1
        entrys -= 1
        increment = 1
        for i in range(entrys): # Adds entry under each column lable where user can enter data
            tempEnter.append(tk.Entry(window))
            tempEnter[-1].grid(row=3,column=increment,padx=10,pady=10)
            increment += 1
        tempButon.append(tk.Button(window,text="Submit",command=lambda:addEntry(tableSelected,columns))) #Button to Submit selection and move to next step
        tempButon[-1].grid(row=4,column=1,padx=10,pady=10)

def addEntry(tableSelected,columns): # adds entry to table and displays it
    columData = {}
    for i in range(len(columns)): # creats dictionary with each column and its data
        columData.update({columns[i]:tempEnter[i].get()})
    #print(columData)
    clearWindow()
    sqlData(tableSelected,columData) # creats data entry and adds it to the table
    if tablesInDatabase[tableSelected].columData[columns[0]] == "tinytext" or tablesInDatabase[tableSelected].columData[columns[0]] == "mediumtext": # adds '' to strings for sql to read
        surch = f"'{columData[columns[0]]}'"
    else:
        surch = columData[columns[0]]
    result = surchTable(tableSelected,columns[0],surch) # finds entry in sql table to confirm creation
    instructionsText.set(result[0])
    tempButon.append(tk.Button(window,text='Menu',command=startOptionSelect)) # Button to return back to main menu
    tempButon[-1].grid(row=2,column=1,padx=10,pady=10)


def continueEditColum(table,editID): # Finds column of the data to be changed
    clearWindow()
    colum = tk.StringVar(window)
    instructionsText.set("Select column of the data you want to change")
    a=1
    for column in tablesInDatabase[table].columData:# iterates through all columns in selected table and creats radio buttons to select column
        tempRadio.append(tk.Radiobutton(window,variable=colum,value=column,text=column))
        tempRadio[-1].grid(row=2,column=a,padx=10,pady=10)
        a+=1
    colum.set('id')
    tempButon.append(tk.Button(window,text="Submit",command=lambda:continueEditData(table,editID,colum.get()))) #Button to Submit selection and move to next step
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)

def continueEditData(table,editID,editColumn): # gets the new data from the user
    clearWindow()
    instructionsText.set("Enter the data you would like have")
    tempEnter.append(tk.Entry(window))
    tempEnter[0].grid(row=2,column=1,pady=10,padx=10)
    tempButon.append(tk.Button(window,text="Submit",command=lambda:editColum(table,editID,editColumn,tempEnter[0].get()))) #Button to Submit selection and move to next step
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)

def continueSurchData(tableSelected,surchData): # gets the known data from the user
    clearWindow()
    instructionsText.set("Enter the data you are looking for")
    tempEnter.insert(0,tk.Entry(window))
    tempEnter[0].grid(row=2,column=1,pady=10,padx=10)
    tempButon.append(tk.Button(window,text="Submit",command=lambda:continueSurchFindNum(tableSelected,surchData,tempEnter[0].get()))) #Button to Submit selection and move to next step
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)

def continueSurchFindNum(tableSelected,surchData,data):# gets the numbers of columns that the user wants to have returned
    clearWindow()
    instructionsText.set("How many column would you like to have shown")
    if tablesInDatabase[tableSelected].columData[surchData[0]] == 'tinytext' or tablesInDatabase[tableSelected].columData[surchData[0]] == 'mediumtext':
        data = f"'{data}'"
    surchData.append(data)
    #print(surchData)
    chose = tk.IntVar(window)
    a=1
    for num in range(len(tablesInDatabase[tableSelected].columData)): # adds a radio button for each number
        if num == len(tablesInDatabase[tableSelected].columData)-1:# last number is diabllaed as all
            tempRadio.append(tk.Radiobutton(window,variable=chose,value=num+1,text='All'))
            tempRadio[-1].grid(row=4,column=a,padx=10,pady=10)
        else:
            tempRadio.append(tk.Radiobutton(window,variable=chose,value=num+1,text=num+1))
            tempRadio[-1].grid(row=4,column=a,padx=10,pady=10)
        a+=1
    tempButon.append(tk.Button(window,text='Submit',command=lambda:continueSurchFindColum(tableSelected,surchData,chose.get(),0,[]))) #Button to Submit selection and move to next step
    tempButon[-1].grid(row=3,column=1,padx=10,pady=10)


def continueSurchFindColum(tableSelected,surchData,num,loopNum,findColums,add=None): # find each column the uares want to see
    clearWindow()
    instructionsText.set("Select the columns you want to see one at a time, press enter between each column")
    if add != None: # adds previusly selected column to column list
        findColums.append(add)
    if num == len(tablesInDatabase[tableSelected].columData):# if user selected to see all columns skips right to displying the data
        startSurch(tableSelected,surchData[0],surchData[1],'*')
    elif loopNum == num: # once all columns are selected moves on to dislaying data
        startSurch(tableSelected,surchData[0],surchData[1],findColums)
    else:
        colum = tk.StringVar(window)
        a=1
        for column in tablesInDatabase[tableSelected].columData:# iterates through all columns in selected table and creats radio buttons to select column
            if column in findColums:
                continue
            tempRadio.append(tk.Radiobutton(window,variable=colum,value=column,text=column))
            tempRadio[-1].grid(row=2,column=a,padx=10,pady=10)
            a+=1
        colum.set('id')
        tempButon.append(tk.Button(window,text='Submit',command=lambda:continueSurchFindColum(tableSelected,surchData,num,loopNum+1,findColums,colum.get()))) #Button to Submit selection and move to next step
        tempButon[-1].grid(row=3,column=1,padx=10,pady=10)


'''
tempEnter.insert(1,tk.Entry(window))
tempEnter[1].grid(row=3,column=2,pady=10,padx=10)
tempEnter.insert(2,tk.Entry(window))
tempEnter[2].grid(row=3,column=3,pady=10,padx=10)
'''
#tempButon.insert(0,tk.Button(window,text="surch",command=lambda:startSurch(tableSelected,colum.get(),tempEnter[0].get(),tempEnter[2].get())))
#tempButon[0].grid(row=3,column=4,pady=10,padx=10)

def editColum(table,editID,editcolumn,editData): # edits the selected entry and dislays it
    clearWindow()
    if tablesInDatabase[table].columData[editcolumn] == "tinytext" or tablesInDatabase[table].columData[editcolumn] == "mediumtext": # adds '' to string for sql to read it as one
        editData = f"'{editData}'"
    changeEntry(table,editID,editcolumn,editData)
    entery = surchTable(table,editcolumn,editData)
    instructionsText.set(entery[0])
    tempButon.append(tk.Button(window,text='Menu',command=startOptionSelect)) # Button to return back to main menu
    tempButon[-1].grid(row=2,column=1)

def startSurch(table, colum, data, findlist): # shows result of surch
    clearWindow()
    find = ', '.join(findlist)
    result = surchTable(table,colum,data,find)
    #print(result,table, colum, data, find)
    if result == []:# if nothing was found
        tempLable.append(tk.Label(window,text=f"No {data} was found in column {colum} of table {table}"))
        tempLable[-1].grid(row=3,column=1,pady=10,padx=10)
    else: # displas all results if the was multiple
        for i in range(len(result)):
            tempLable.append(tk.Label(window,text=result[i]))
            tempLable[-1].grid(row=3+i,column=1,pady=3,padx=10)
    tempButon.append(tk.Button(window,text='Menu',command=startOptionSelect)) # Button to return back to main menu
    tempButon[-1].grid(row=2,column=1)

def tableSelect(option): #return what table is selected, runs for all option paths, passes through selected option for next function
    #next fuction in chain is continueOption() line 180
    global tableSelected
    instructionsText.set("Select Table")
    tableSelected = tk.StringVar(window)
    a = 0
    tempLable.append(tk.Label(window,text='You have Selected:'))
    tempLable[-1].grid(row=3,column=1)
    tempLable.append(tk.Label(window,textvariable=tableSelected))# shows selected table
    tempLable[-1].grid(row=3,column=2)
    for table in tablesInDatabase:# adds a radio button for each table in the data base
        tempRadio.append(tk.Radiobutton(window,variable=tableSelected,value=table,text=table))
        tempRadio[a].grid(row=2,column=1+a,padx=10,pady=10)
        tableSelected.set(table)
        a += 1
    tempButon.append(tk.Button(window,text='Submit',command=lambda:continueOption(option,tableSelected.get()))) #Button to Submit selection and move to next step
    tempButon[-1].grid(row=3,column=3) 
    
def startoption(option):#Hides the main menu by forgeting grid placment
    clearWindow()
    surchButton.grid_forget()
    editButton.grid_forget()
    createButton.grid_forget()
    tableSelect(option)

#main menu elements
surchButton = tk.Button(window,text='Surch for record in a table',command=lambda:startoption('surch'))
editButton = tk.Button(window,text='Edit table record',command=lambda:startoption('edit'))
createButton = tk.Button(window,text='Add new record to a table',command=lambda:startoption('create'))

def startOptionSelect():#Shows the main menu
    clearWindow()
    instructionsText.set("Select Option")
    surchButton.grid(column=1,row=2,padx=10,pady=10)
    editButton.grid(column=2,row=2,padx=10,pady=10)
    createButton.grid(column=3,row=2,padx=10,pady=10)

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
"""
#first test of temperary buttons
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

reAddTable()
startOptionSelect()
window.mainloop()