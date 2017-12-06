import sqlite3
from random import randint
def create_tables():
    conn = sqlite3.connect('test.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INT UNIQUE,
                verified BOOLEAN,
                code VARCHAR(50),
                email VARCHAR(50)
            );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS chats(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first INT,
                second INT
            );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS questions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value INT NOT NULL
            );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS responce(
                id INT PRIMARY KEY NOT NULL,
                value INT NOT NULL,
                question_id INT,
                FOREIGN KEY(question_id) REFERENCES questions(id)
            );''')
    print("TABLES created successfully");
    conn.close()

def drop_tables():
    conn = sqlite3.connect('test.db')
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("DROP TABLE IF EXISTS chats")
    conn.execute("DROP TABLE IF EXISTS questions")
    conn.execute("DROP TABLE IF EXISTS responce")
    print("ALL TABLES DROPED");
    conn.close()


def get_user(chat_id):
    conn = sqlite3.connect('test.db')
    rows = conn.execute('SELECT * FROM users WHERE chat_id=?', (chat_id,))
    row = rows.fetchone()
    conn.close()
    return row

# if already exists returns false
def create_user(chat_id, verified, email):
    res = get_user(chat_id)
    conn = sqlite3.connect('test.db')

    if(res == None):
        conn.executemany("insert into users (chat_id, verified, email) values (?,?,?);", [(chat_id, verified, email,),])
        conn.commit()
        conn.close()
        return True
    else:
        conn.close();
        return False

# update user, second and third values are change values
def update_user(chat_id, verified, email, code):
    res = get_user(chat_id)
    conn = sqlite3.connect('test.db')
    if(res != None):
        conn.executemany("UPDATE users SET verified = ?, email = ?, code = ? WHERE chat_id = ?", [(verified, email, code, chat_id,),])
        conn.commit()
        conn.close()
        return True
    else:
        conn.close();
        return False
    conn.executemany("insert into users (chat_id, verified, email) values (?,?,?);", [(chat_id, verified, email,),])
    


def create_chat(first, second):
    conn = sqlite3.connect('test.db')
    conn.executemany("insert into chats (first, second) values (?,?);", [(first, second,),])
    conn.commit()
    conn.close()


def show_users():
    conn = sqlite3.connect('test.db')
    rows = conn.execute('SELECT * FROM users')
    rows = rows.fetchall()
    print(rows)
    conn.close()

def show_chats():
    conn = sqlite3.connect('test.db')
    rows = conn.execute('SELECT * FROM chats')
    rows = rows.fetchall()
    print(rows)
    conn.close()

def is_verified(chat_id):
    res = get_user(chat_id)
    conn = sqlite3.connect('test.db')

    if(res == None):
        conn.close();
        return False
    else:
        return bool(res[2])

def remove_chat(chat_id):
    conn = sqlite3.connect('test.db')
    conn.execute("delete from chats where first = (?);", (chat_id,))
    conn.execute("delete from chats where second = (?);", (chat_id,))
    conn.commit()
    conn.close()

def get_chat(chat_id):
    conn = sqlite3.connect('test.db')
    rows = conn.execute('SELECT * FROM chats WHERE first=?', (chat_id,))
    rows = conn.execute('SELECT * FROM chats WHERE second=?', (chat_id,))
    row = rows.fetchone()
    conn.close()
    return row

def create_question(value):
    conn = sqlite3.connect('test.db')
    conn.execute("insert into questions (value) values (?);", (value,))
    conn.commit()
    conn.close()

def show_questions():
    conn = sqlite3.connect('test.db')
    rows = conn.execute('SELECT * FROM questions')
    rows = rows.fetchall()
    print(rows)
    conn.close()

# returns 10 top questions
def get_questions():
    conn = sqlite3.connect('test.db')
    rows = conn.execute("select count(*) from questions")
    rows_num = rows.fetchone()[0]
    res = []
    while(len(res) != 3):
        elem = randint(1, 6)
        rows = conn.execute('SELECT * FROM questions WHERE id=?', (elem,))
        row = rows.fetchone()
        res.append(row)
    conn.close()
    return res