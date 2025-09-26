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
                   pr text not null references books(id),
                   completed integer not null default (0))
    """)

    cursor.execute(""" create table if not exists Appl_Serv (
                   id integer primary key autoincrement,
                   application_id integer not null references application(id) on delete cascade
                                                                               on update cascade,
                   service_id integer not null references service(id) on delete cascade
                                                                      on update cascade)
    """)

    connect.commit()

#create_table()


def insert_SQL():
    cursor.execute(""" insert into Service (name)
    values ('flute'), ('guitar'),('piano'),('violin'),('drums')
    """)

    cursor.execute(""" insert into Master (name, surname, age, category)
    values ('Ivan','Ivanov',37,2), ('Jackson','Smith',23,4),('Ana','Agapova',20,5),('Barbara','Tyler',64,3)
    """)
    connect.commit()

#insert_SQL()


def insert_cart():
    item_A = [(1,1),(2,0),(3,1),(4,0)]
    item_A_S = [(1,2),(1,3),(1,5),(2,4),(3,5),(3,1)]

    cursor.executemany(""" insert into Application (master_id,completed)
    values (?,?)""", item_A)

    cursor.executemany(""" insert into Appl_Serv (application_id,service_id)
    values (?,?)""", item_A_S)
    connect.commit()

#insert_cart()


def update_M():
    cursor.execute(""" update Master
    set category = ?
    where id = ?
    """, (int(input()),int(input())))
    connect.commit()

#update_M()


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
    """, (int(input()),))    #Можно задать конкретную услугу, но мне кажется так удобнее)
    connect.commit()

#delete_S()


def select_Categ():
    cursor.execute(""" select * from Master
    where category > 3
    """)
    for row in cursor.fetchall():
        print(*row)  #Здесь и дальше добавила * чисто для красоты)

#select_Categ()


def select_Age():
    cursor.execute(""" select count(age) from Master
    where age > 35
    """)
    for row in cursor.fetchall():
        print(*row)

#select_Age()


def select_Appl():
    cursor.execute(""" select name from Service
    left join Appl_Serv on service_id = service.id
    where application_id = ?
    """, (int(input()),))
    for row in cursor.fetchall():
        print(*row)

#select_Appl()


def select_Mas():
    cursor.execute(""" select Application.id from Application
    left join Master on Application.master_id = Master.id
    where Master.name = ? and Master.surname = ?
    """, (input(),input()))
    for row in cursor.fetchall():
        print(*row)

#select_Mas()


def select_NotDone():
    cursor.execute(""" select Application.id, Master.name, Master.surname from Application
    left join Master on Application.master_id = Master.id
    where Application.completed = 0
    """)
    for row in cursor.fetchall():
        print(*row)
        
#select_NotDone()