import sqlite3

from model.api_user import ApiUser
con = sqlite3.connect("volumes/database.db")

def init():
  cursor = con.cursor()
  query = """CREATE TABLE IF NOT EXISTS API_LOG(
              api_key TEXT,
              request_date DATETIME,
              endpoint TEXT,
              status TEXT
            )"""
  cursor.execute(query)
  cursor.close()

def insert(api_key, request_date, endpoint, log):
    cursor = con.cursor()
    query = f"""INSERT INTO API_LOG (api_key, request_date, endpoint, status)
              VALUES ('{api_key}', '{request_date}', '{endpoint}', '{log}')"""
    cursor.execute(query)
    con.commit()
    cursor.close()
    