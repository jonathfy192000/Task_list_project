import sqlite3


def view_task(connection):
    cursor = connection.cursor()
    gather_table = """SELECT * from Assignments"""
    cursor.execute(gather_table)
    data = cursor.fetchall()
    
    for row in data:
        name = row[0]
        start_date = row[1]
        due_date = row[2]
        summary = row[3]
        tips = row[4]
        print(row)
    cursor.close()
    
def add_task(connection):
    cursor = connection.cursor()
    #want to open a window here with 4 boxes, Name: , Start date: , Due Date: , Summary: , Tips:, on GUI, won't need "input", so if the input box is empty then it stays as ""
    n = input("Name: \n")
    s_date = input("Start date: \n")
    d_date = input("Due date: \n")
    summ = input("Summary: \n")
    tip = input("Tips: \n")

    tuple_data = (n, s_date, d_date, summ, tip)
    insert_query = """INSERT INTO Assignments(name, start_date, due_date, summary, tips) VALUES(?, ?, ?, ?, ?)"""
    cursor.execute(insert_query, tuple_data)
    connection.commit()
    cursor.close()

def delete_task(connection):
    cursor = connection.cursor()
    to_delete = input("Name of task to delete: ")
    delete_query = """DELETE FROM Assignments WHERE name=?"""
    cursor.execute(delete_query, (to_delete,))
    connection.commit()
    cursor.close()
    
def edit_task(connection):
    #when implementing actual GUI, just fill the input box with what is currently stored, then can just modify that and enter that as new data
    cursor = connection.cursor()
    to_edit = input("Name of task to edit: ")
    n_start = input("New start date: ")
    n_due = input("New due date: ")
    n_summary = input("New summary: ")
    n_tips = input("New tip: ")
    
    edit_query = """UPDATE Assignments SET start_date = ?,
                                            due_date = ?,
                                            summary = ?,
                                            tips = ?
                                            WHERE name = ?"""
    cursor.execute(edit_query, (n_start, n_due, n_summary, n_tips, to_edit))
    connection.commit()
    cursor.close()
    
def view_data(connection):
    cursor = connection.cursor()
    create_table = """CREATE TABLE IF NOT EXISTS Assignments(name text NOT NULL, start_date text NOT NULL, due_date text NOT NULL, summary text, tips text);"""
    try:
        cursor.execute(create_table)
    except sqlite3.Error as e:
        print(e)

    command = input("Enter command: (View/Add/Delete/Edit/Back)\n").lower() #back is not implemented, back is for when the user wants to view a different class
    
    while command != "back":
        #once table is created, want to display the table and edit if wanted
        if command == "view":
            view_task(connection)
                
        elif command == "add":
            add_task(connection)

        elif command == "delete":
            delete_task(connection)
            
        elif command == "edit":
            edit_task(connection)
        #don't need else because commands will be buttons on the GUI
        command = input("Enter command: (View/Add/Delete/Edit/Back)\n").lower()
    
    
