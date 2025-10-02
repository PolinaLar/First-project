import sqlite3

connect = sqlite3.connect("project.db") 
cursor = connect.cursor()

def add_book(title, author, genre, n=1): #Работает!)
    cursor.execute("""select * from books
                   where title = ? and author = ?""", (title, author)) #выбираю из books ту, которую задали
    if cursor.fetchone():#если такая есть, то update
        cursor.execute("""update books
                    set total = total + ?, free = free + ?
                    where title = ? and author = ?""", (n, n, title, author))
    else: #если нет, то вот insert
        cursor.execute("""insert into books (title, author, genre, total, free)
                    values (?,?,?,?,?)""", (title, author, genre, n, n))
    connect.commit()

#add_book("Грозfwа", "Островский", "комедия", 1)
    
def delete_book(title, author): #тут точно также #Работает!)
    cursor.execute("""select total, free from books
                   where title = ? and author = ?""", (title, author))
    row = cursor.fetchone()
    if (row):
        total, free = row[0], row[1]
        cursor.execute("""select * from holds
                        join books on holds.book_id = books.id
                        where title = ? and author = ?""", (title, author))
        if (total == free and cursor.fetchone() == None): #первое условие на loan (если все свободные, значит никто не взял), второе на hold
            cursor.execute(""" delete from books
                            where title = ? and author = ?""", (title, author))
    else:
        print("Сорян, но книгу нельзя удалить :(") #это не просили, я сделала чисто для проверки
    connect.commit()

#delete_book("Звездные воины","Дартвейдер")

def generate_num(full_name, phone): #Ну это тоже работает)) 
    full_name = full_name.split(" ")
    return full_name[0][0]+full_name[1][0]+str(len(full_name[0]))+str(len(full_name[1]))+phone[-4:]

#print(generate_num("Полина Ларионова", "89588021122"))

def add_reader(full_name, phone, age): #Работает!)
    cursor.execute(""" insert into readers (pr,full_name, phone, age)
        values (?,?,?,?)""", (generate_num(full_name, phone), full_name, phone, age))
    connect.commit()

#add_reader("Вася Васильев", "89990122200", 72)

def delete_reader(pr): #Работает!))
    cursor.execute("""select * from holds
                    join readers on holds.pr = readers.pr
                    where holds.pr = ?""", (pr,))
    hold = cursor.fetchone()
    cursor.execute("""select * from loans
                    join readers on loans.pr = readers.pr
                    where loans.pr = ?""", (pr,))
    loan = cursor.fetchone()
    if hold or loan:
        print("Пользователя пока нельзя удалить -_-")
    else:
        cursor.execute(""" delete from readers
                    where pr = ? """,(pr,))
    connect.commit()

#delete_reader("ВВ482200")