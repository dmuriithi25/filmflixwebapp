import sqlite3   #Importing sqlite3 library 

connection = sqlite3.connect('filmFlix.db') #connecting sqlite3 with the Db

with open('schema.sql') as f:       #linking to the schema.sql file and naming under the f variable
    connection.executescript(f.read())   #executing read function to read contents of the f file (schema.sql)

    cur = connection.cursor()    #created a cursor object

    cur.execute("INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?)",
                   ('The Bourne Identity', '2002', 'PG', '220', 'Thriller/Action')
                   )        #INSERT values to the the SQL database
    
    cur.execute("INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?)",
                   ('Kung Fu Panda', '2008', 'PG', '90', 'Family/Comedy')
                   )
    
    connection.commit()     #commit changes
    connection.close()      #close the connection to the database
