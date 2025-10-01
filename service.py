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
        where id = ?""", (count-1,book_id))
    
    connect.commit()
print(datetime.now().strftime("%d/%m/%y"))
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
        set free = ?
        where id = ?""", (book_free+1,book_id))
    
    connect.commit()

#delete_hold("ПЛ691122", "Евгений Онегин", "Пушкин")