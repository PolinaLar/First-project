from datetime import datetime
import sqlite3

connect = sqlite3.connect("project.db")
cursor = connect.cursor()
def book(pr, title, author):
    date = datetime.now().strftime("%d/%m/%y")
    cursor.execute("""select * from books
                   where title = ? and author = ?""",(title, author))
    
    book_1 = cursor.fetchone()
    book_id = book_1[0]
    book_free = book_1[5]
    cursor.execute("""select count(*) from holds
                   where pr == ?
                   group by pr""",(pr,))
    count = cursor.fetchone()[0]
    if (book_free > 0 and count < 5):
        cursor.execute("""insert into holds (pr,book_id,date)
        values (?,?,?)""", (pr,book_id,date))
        
        cursor.execute(""" update books
            set free = ?
            where id = ?""", (book_free-1,book_id))
    
    connect.commit()
#book("ПЛ691122", "Евгений Онегин", "Пушкин")


def delete_hold(pr, title, author):
    cursor.execute("""select * from books
                   where title = ? and author = ?""",(title, author))
    book = cursor.fetchone()
    book_id = book[0]
    book_free = book[5]

    cursor.execute(""" delete from holds
    where pr = ? and book_id = ?
    """, (pr,book_id))
    
    cursor.execute(""" update books
        set free = free + 1
        where id = ?""", (book_id,))
    
    connect.commit()

#delete_hold("ПЛ691122", "Евгений Онегин", "Пушкин")

def loans(pr, title, author):
    cursor.execute("""select * from books
                   where title = ? and author = ?""",(title, author))
    
    book = cursor.fetchone()
    book_id = book[0]
    book_free = book[5]

    cursor.execute("""select count(*) from loans
                   where pr == ?
                   group by pr""",(pr,))
    
    cur = cursor.fetchone()
    if (cur):
        count = cur[0]
    else:
        count = 0
    if (book_free > 0 and count < 5):
        cursor.execute(""" update books
        set free = free - 1
        where id = ?""", (book_id,))

        cursor.execute("""select title, author, book_id from books
                    join holds on holds.book_id = books.id
                    where pr == ?""",(pr,))
        for hold in cursor.fetchall():
            if (hold[0] == title and hold[1] == author):
                cursor.execute("""delete from holds
                    where book_id = ? and pr = ?""", (hold[2], pr))
                break
        cursor.execute("""insert into loans (pr,book_id,date)
            values (?,?,?)""", (pr,book_id,datetime.now().strftime("%d/%m/%y")))
    
    connect.commit()
def return_book(pr, title, author):
    cursor.execute("""select book_id from books
    where title = ? and author = ?""", (title, author))
    row = cursor.fetchone()
    cursor.execute("""delete from loans
    where book_id = ? and pr = ?""", (row[0], pr))
    cursor.execute("""update books
    set free += 1
    where book_id = ?""", (row[0]))
    connect.commit()

def taken_books(pr):
    cursor.execute("""select title, author, date_loan, date_return from loans
    where pr = ?""", (pr))
    return cursor.fetchall()
    connect.commit()

def held_books(pr):
    cursor.execute("""select title, author, date_hold, expires_at from holds
    where pr = ?""", (pr))
    return cursor.fetchall()
    connect.commit()

loans("ЮА470011", "Гроза", "Островский")
