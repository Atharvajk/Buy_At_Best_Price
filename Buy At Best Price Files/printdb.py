import sqlite3
#printing main databse file
def printdb():
    conn = sqlite3.connect('MY_Products.db')
    # Create cursor
    c = conn.cursor()

    # query the db
    c.execute("SELECT rowid, * FROM myProducts")
    records = c.fetchall()
    
    #print(records)
    for record in records:
        print(record)
printdb()