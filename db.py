import sqlite3

connect = sqlite3.connect("homework.db")
cursor = connect.cursor()

def create_table():
    cursor.execute(""" create table if not exists readers (
                   pr text primary key,
                   full_name text not null
                   phone text not null
                   ahe integer not null)
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
                   book_id integer not null references boks(id),
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


def insert_cart():
    item_A = [(1,1),(2,0),(3,1),(4,0)]
    item_A_S = [(1,2),(1,3),(1,5),(2,4),(3,5),(3,1)]

    cursor.executemany(""" insert into Application (master_id,completed)
    values (?,?)""", item_A)

    cursor.executemany(""" insert into Appl_Serv (application_id,service_id)
    values (?,?)""", item_A_S)
    connect.commit()

#insert_cart()

def update_A():
    cursor.execute(""" update Application
    set completed = 1
    where id = ?
    """, (int(input()),))
    connect.commit()

#update_A()


def delete_S():
    cursor.execute(""" delete from Service
    where id = ?
    """, (int(input()),))
    connect.commit()

#delete_S()


def select_NotDone():
    cursor.execute(""" select Application.id, Master.name, Master.surname from Application
    left join Master on Application.master_id = Master.id
    where Application.completed = 0
    """)
    for row in cursor.fetchall():
        print(*row)
        
#select_NotDone()