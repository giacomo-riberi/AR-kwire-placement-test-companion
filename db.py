
import sqlite3
import secrets
import sys

from logger import logger
from __init__ import *
import data

def db_newid(id_bytes):
    "newid generates a new id string not present on database of specified byte lenght"
    
    def idexist(id):
        "idexist checks if id exists in any table of database"

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE id = ?", (id,))
            count = cursor.fetchone()[0]
            if count > 0:
                return True
        return False
    
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    tmp_id = secrets.token_hex(id_bytes)
    while idexist(tmp_id):
        tmp_id = secrets.token_hex(id_bytes)

    connection.close()

    return tmp_id


def db_save(TEST_data: data.TESTdata):
    "save_db saves data on database"

    try:
        conn = sqlite3.connect(db_name) # Create a connection to the SQLite database (or create it if it doesn't exist)
        cursor = conn.cursor() # Create a cursor object to interact with the database

        # create TEST table
        cursor.execute(TEST_data.db_create_table("TEST"))

        # create ECP table
        cursor.execute(data.ECPs[0].db_create_table("ECP"))

        # create PA table
        cursor.execute(data.PAs[0].db_create_table("PA"))
        
        conn.commit()
    
    
        ### DON'T COMMIT UNTIL ALL INSERTIONS ARE DONE! ###

        # insert TEST_data into database
        cursor.execute(*TEST_data.db_insert_table("TEST"))
        
        # insert ECPs into database
        for ECP_data in data.ECPs:
            cursor.execute(*ECP_data.db_insert_table("ECP"))

        # insert PAs into database
        for PA_data in data.PAs:
            cursor.execute(*PA_data.db_insert_table("PA"))
            
    except sqlite3.Error as er:
        logger.error(f"-------------------")
        logger.error(f"SQLite traceback  : " + " - ".join([str(x).strip() for x in sys.exc_info()]))
        logger.error(f"SQLite error line : " + str(er.__traceback__.tb_lineno))
        logger.error(f"SQLite error      : " + str(er))
        logger.critical(f"\nexiting. DATA NOT SAVED!")
        sys.exit()
        
    conn.commit()
    conn.close()
    logger.info("SAVED ON DATABASE!")
