import sqlite3
import secrets
import sys, os

from logger import logger
from __init__ import *
import data

def db_idexist(id) -> bool:
    # check new_id against database, if exist
    if os.path.exists(db_name):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE id = ?", (id,))
            count = cursor.fetchone()[0]
            if count > 0:
                return True
        connection.close()
    return False

def db_newid(id_bytes):
    "newid generates a new id string not present on database of specified byte lenght"

    # check new_id against database
    new_id = secrets.token_hex(id_bytes)
    while db_idexist(new_id):
        new_id = db_newid(id_bytes)
    
    # check new_id against PHASE, ECP and PA runtime variables
    if data.PHASE_toinsert != None and data.PHASE_toinsert.id == new_id:
        new_id = db_newid(id_bytes)

    for ECP in data.ECPs_toinsert:
        if ECP.id == new_id:
            new_id = db_newid(id_bytes)
    
    for PA in data.PAs_toinsert:
        if PA.id == new_id:
            new_id = db_newid(id_bytes)
    
    return new_id


def db_save_all():
    "save_db saves data on database"

    if len(data.ECPs_toinsert) <= 0 or len(data.PAs_toinsert) <= 0:
        logger.critical("no ECPs/PAs to insert into database!")
        quit()

    try:
        conn = sqlite3.connect(db_name) # Create a connection to the SQLite database (or create it if it doesn't exist)
        cursor = conn.cursor() # Create a cursor object to interact with the database

        # create PHASE table
        cursor.execute(data.PHASE_toinsert.db_create_table("PHASE"))

        # create ECP table
        cursor.execute(data.ECPs_toinsert[0].db_create_table("ECP"))

        # create PA table
        cursor.execute(data.PAs_toinsert[0].db_create_table("PA"))
        
        conn.commit()
    
        ### DON'T COMMIT UNTIL ALL INSERTIONS ARE DONE! ###

        # insert PHASE_data into database
        cursor.execute(*data.PHASE_toinsert.db_insert_table("PHASE"))
        
        # insert ECPs into database
        for ECP_data in data.ECPs_toinsert:
            cursor.execute(*ECP_data.db_insert_table("ECP"))

        # insert PAs into database
        for PA_data in data.PAs_toinsert:
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


def db_update():
    try:
        conn = sqlite3.connect(db_name) 
        cursor = conn.cursor()
        
        prompt = f"ATTENTION! TECHNICAL - enter data from fusion 360 to update PA db entry: "
        user_input = input(prompt)
        PA_data = data.PAdata(**json.loads(user_input))
        if not PA_data.fusion_computed:
            raise Exception("data not computed by fusion")
        
        if not db_idexist(PA_data.id):
            raise Exception("id does NOT exist on database")
        
        logger.debug_input(prompt + "\t|" + user_input + "|")
        
        cursor.execute(PA_data.db_update_table("PA", PA_data.id))
    
    except sqlite3.Error as e:
        logger.error(f"-------------------")
        logger.error(f"SQLite traceback  : " + " - ".join([str(x).strip() for x in sys.exc_info()]))
        logger.error(f"SQLite error line : " + str(e.__traceback__.tb_lineno))
        logger.error(f"SQLite error      : " + str(e))
        logger.critical(f"\nexiting. DATA NOT UPDATED!")
        sys.exit()
    
    except Exception as e:
        logger.error(f"-------------------")
        logger.error(f"{e}")
        logger.critical(f"\nexiting. DATA NOT UPDATED!")
    
    conn.commit()
    conn.close()
    logger.info(f"UPDATED DATABASE PA entry {PA_data.id}!")