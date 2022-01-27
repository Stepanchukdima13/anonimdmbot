import sqlite3
from sqlite3 import Error

def get_connection():
    global connection
    try:
        connection = sqlite3.connect("database.db")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute("DROP TABLE IF EXISTS questions")
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions(
        "firstname"          TEXT,
    	"username"	         TEXT,
    	"userid"             TEXT,
    	"recipientFirstname" TEXT,
    	"recipientUsername"  TEXT,
    	"recipientUserId"    TEXT,
    	"question"           TEXT,
    	"time"               TEXT
    )''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS userdata(
        	"username"	    TEXT,
        	"userid"        TEXT
        )''')




def add_question(firstname,username: str, userid,recipientFirstname,recipientUsername,recipientUserId,question,time):
    conn = get_connection()
    c = conn.cursor()

    c.execute('''INSERT OR IGNORE INTO questions (firstname,username, userid,recipientFirstname,recipientUsername,recipientUserId,question,time) VALUES (?,?,?,?,?,?,?,?)''',
              (firstname,username, userid,recipientFirstname,recipientUsername,recipientUserId,question,time))
    conn.commit()

def add_user(firstname: str, userid):
    conn = get_connection()
    c = conn.cursor()
    useridarr = get_all_userid()
    for oneUserId in useridarr:
        if int(userid) == int(oneUserId):
            return False  # Якщо знайдено однакові ключі
    c.execute('''INSERT OR IGNORE INTO userdata (firstname, userid) VALUES (?,?)''',
                (firstname, userid))
    conn.commit()

def get_all_userid():
    arrId = []
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT userid FROM userdata""")
    my_data = c.fetchall()
    for data in my_data:
        arrId.append(data[0])
    return arrId
