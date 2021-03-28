import sqlite3
import db_modification

def sqlite_connect(database_n):
    try:
        connection = sqlite3.connect(database_n)
    except:
        print("Error connecting to the database {}!".format(database_n))
    return connection

def create_table(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)

#see if the school name exists in the name table, if not give the choice to create
#an entry for the school, otherwise do nothing
def search_table(database, school_name):
    #table name == "schools"
    connection = sqlite_connect(database)
    cursor = connection.cursor()

    try:
        find_q = "SELECT * FROM schools WHERE name=?"
        cursor.execute(find_q, (school_name,))
        print("found")
        return True
    except:
        print("School does not currently exist")
        print("Would you like to create entry for this school?(Yes/No)")
        entry = input("Yes/No: ")
        if entry == "Yes":
            query = """INSERT INTO schools(name) VALUES(?)"""
            n_tuple = (school_name,)
            cursor.execute(query, n_tuple)
            connection.commit()
            #create a table for that school in schools db
            create_query = """CREATE TABLE IF NOT EXISTS {}(department_name text NOT NULL, course_name text NOT NULL);""".format(school_name)
            try:
                create_table(connection, create_query)
                print("School created")
                return True
            except sqlite3.Error as e:
                print(e)
        connection.commit()
        cursor.close()
        connection.close()
        return False
            

def print_courses(name):
    course_view = sqlite_connect("schools.db")
    course_query = """SELECT * FROM {}""".format(name)
    cursor = course_view.cursor()
    cursor.execute(course_query)
    rows = cursor.fetchall()
    for row in rows:
        print("{}: {}".format(row[0], row[1]))
    course_view.commit()
    cursor.close()
    course_view.close()
    
def add_course(name):
    course_view = sqlite_connect("schools.db")
    add_query = """INSERT INTO {}(department_name, course_name) VALUES(?, ?)""".format(name)
    add_course = input("Enter coursename\n").lower()
    add_department = input("Enter department\n").lower()
    cursor = course_view.cursor()
    cursor.execute(add_query, (add_course, add_department))
    course_view.commit()
    cursor.close()
    course_view.close()
    
if __name__ == "__main__":
    name = input("Enter your school\n")
    #search up the schoolname in the school database
    name_exists = search_table("schools.db", name)
    
    #show the current courses available
    print_courses(name)

    #have a + button at the bottom to add a course
    course_name = input("Enter your coursename\n").lower()
    try:
        conn = sqlite_connect("schools.db")
        query = """SELECT * FROM {} WHERE course_name=?""".format(name)
        cursor = conn.cursor()
        cursor.execute(query, (course_name,))
        exists = cursor.fetchall()
        
        if (len(exists) == 0): #course does not exist
            print("Course not found")
            add_course(name)
    except sqlite3.Error as e:
        print(e)
                       
    
    db_connection = sqlite_connect("{}_{}.db".format(name, course_name))
    
    #now find the data you want from the table
    db_modification.view_data(db_connection)
    


