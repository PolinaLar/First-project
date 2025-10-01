import sqlite3

connect = sqlite3.connect("project.db") 
cursor = connect.cursor()

def add_book(title, author, genre, n): 
    cursor.execute(""" update books
                   set total += ?, free += ?
                   where title is not null and author is not null
                   set total = 1, free = 1, title = ?, author = ?, genre = ?
                   where title is null and author is null """, n, 
                   n, title, author, genre)
    
def delete_book(title, author):
    cursor.execute(""" delete from books
                   where (title = ?, author = ?)
                   if not exists (pr.loans, pr.holds)""", title, author)

def add_reader(pr, full_name, phone, age):
    cursor.executemany(""" insert into readers (pr,full_name, phone, age)
        values (?,?,?)""", pr,full_name, phone, age)

def delete_reader(pr):
    cursor.execute(""" delete from readers
                   where pr = ? """, pr)
