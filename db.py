import sqlite3

connect = sqlite3.connect("project.db")
cursor = connect.cursor()

def create_table():
    cursor.execute(""" create table if not exists readers (
                   pr text primary key,
                   full_name text not null,
                   phone text not null,
                   age integer not null)
    """)

    cursor.execute(""" create table if not exists books (
                   id integer primary key autoincrement,
                   title text not null,
                   author text not null,
                   genre text not null,
                   total integer not null check(total>=1),
                   free integer not null check (free >=0 and free <= total))
    """)

    cursor.execute(""" create table if not exists loans (
                   id integer primary key autoincrement,
                   pr text not null references readers(pr),
                   book_id integer not null references books(id),
                   date text not null)
    """)

    cursor.execute(""" create table if not exists holds (
                   id integer primary key autoincrement,
                   pr text not null references readers(pr),
                   book_id integer not null references books(id),
                   date text not null)
    """)

    connect.commit()

create_table()

def ganarate_num():
    cursor.execute(" select full_name, phone from readers")
    for row in cursor.fetchall():
        name = row[0].split(" ")
        ans = name[0][0]+name[1][0]+str(len(name[0]))+str(len(name[1]))+row[1][-4:]
        with open("README.md", "w", encoding="utf-8") as file:
            file.write(ans)