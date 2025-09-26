import db
import sqlite3

connect = sqlite3.connect("homework.db") 
cursor = connect.cursor()

def add_book(): 
    cursor.execute(""" update books
                   set total +=1, free += 1
                   if exists (title, author)
                   else  set total = 1, free = 1""")
    
def delete_book():
    cursor.execute(""" delete from books
                   where id = ?
                   if not exists (pr.loans, pr.holds)""", int(input()))

