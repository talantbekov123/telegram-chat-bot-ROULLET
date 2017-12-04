import sqlite3

def create_tables():
    conn = sqlite3.connect('test.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                chat_id INT,
                verified BOOLEAN,
                email VARCHAR(50)
            );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS chats(
                id INT PRIMARY KEY NOT NULL,
                fist INT NOT NULL,
                second INT NOT NULL
            );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS questions(
                id INT PRIMARY KEY NOT NULL,
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


def find_user(chat_id):
    conn = sqlite3.connect('test.db')
    print(chat_id)
    rows = conn.execute('SELECT * FROM users WHERE chat_id=?', (chat_id,))
    rows = rows.fetchall()
    conn.close()
    return rows

def create_user(chat_id,verified,email):
    conn = sqlite3.connect('test.db')
    print(type(chat_id))
    conn.executemany("insert into users (chat_id, verified, email) values (?,?,?);", [(chat_id, verified, email,),])
    conn.commit()
    conn.close()