import sqlite3

connect = sqlite3.connect("project.db")
cursor = connect.cursor()
def book(pr, title, date):
    cursor.execute("""select * from books
                   where title = ?""",(title,))
    
    book_1 = cursor.fetchone()
    title_id = book_1[0]
    if (book_1[5] > 0):
        cursor.executemany(""" insert into holds (pr,book_id,date)
        values (?,?,?)""", pr,title_id,date)

    cursor.execute(""" update books
    set total -= 1
    where id = ?
    """, (title_id,))
    connect.commit()