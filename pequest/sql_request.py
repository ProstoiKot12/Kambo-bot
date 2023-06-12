import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error


con = psycopg2.connect(user="postgres",
                       database='kambodb',
                       password="momo1430",
                       host="localhost",
                       port="5432")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

async def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS user_table(
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    user_name TEXT
                    )''')
    con.commit()

async def insert_into_id(user_id, user_name):
    cur.execute("SELECT * FROM user_table WHERE user_id = %s", (user_id,))
    user1 = cur.fetchone()
    if not user1:
        cur.execute("INSERT INTO user_table (user_id, user_name) VALUES (%s, %s)", (user_id, f"@{user_name}"))
        con.commit()

async def get_user_id():
    cur.execute("SELECT user_id FROM user_table")
    user_id = cur.fetchall()
    return user_id
