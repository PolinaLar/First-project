import db
import sqlite3

connect = sqlite3.connect("project.db") 
cursor = connect.cursor()

def add_book(title, author, genre, n=1): 
    cursor.execute("""insert into books (title, author, genre, total, free)
                   values (?,?,?,?,?)""" (title, author, genre, 1, n))
    connect.commit()
    
def delete_book(title, author):
    cursor.execute(""" delete from books
                    where title = ? and author = ?""", title, author)
    connect.commit()

def add_reader(full_name, phone, age):
    cursor.execute(""" insert into readers (pr,full_name, phone, age)
        values (?,?,?)""", (db.generate_num(full_name, phone), full_name, phone, age))
    connect.commit()

def delete_reader(pr):
    cursor.execute(""" delete from readers
                   where pr = ? """, pr)
    connect.commit()

add_book("Гроза", "Островский", "стихотворение", 1)