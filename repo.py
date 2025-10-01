import db
import sqlite3

connect = sqlite3.connect("homework.db") 
cursor = connect.cursor()

def add_book(title, author, genre, n): 
    cursor.execute(""" update books
                   if exists (title, author) set total += ?, free += ?
                   else  set total = 1, free = 1, title = ?, author = ?, genre = ?""", n, 
                   n, title, author, genre)
    
def delete_book():
    cursor.execute(""" delete from books
                   where id = ?
                   if not exists (pr.loans, pr.holds)""", int(input()))

def add_reader(pr, full_name, phone, age):
    cursor.executemany(""" insert into readers (pr,full_name, phone, age)
        values (?,?,?)""", pr,full_name, phone, age)
