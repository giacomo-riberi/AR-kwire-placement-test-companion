
import sqlite3
import secrets
import sys
from datetime import datetime

from utils.utils import logger
from __init__ import *

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


def db_save(TEST_data):
    "save_db saves data on database"

    global ECPs, PAs

    try:
        conn = sqlite3.connect(db_name) # Create a connection to the SQLite database (or create it if it doesn't exist)
        cursor = conn.cursor() # Create a cursor object to interact with the database

        # create TEST table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TEST (
                id TEXT NOT NULL PRIMARY KEY,
                datatype TEXT,
                PA_ids TEXT,
                ECP_ids TEXT,
                time_init TIMESTAMP,
                phase INTEGER,
                name TEXT,
                surname TEXT,
                gender TEXT,
                age INTEGER,
                specialization_year TEXT,
                num_operations INTEGER,
                test_duration REAL,
                test_radiation REAL,
                test_PAC INTEGER,
                test_PACF INTEGER,
                test_ECPC INTEGER
            )''')

        # create ECP table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ECP (
                id TEXT NOT NULL PRIMARY KEY,
                datatype TEXT,
                test_id TEXT,
                PA_ids TEXT,
                time_init TIMESTAMP,
                phase INTEGER,
                ECP_number INTEGER,
                ECPD REAL,
                ECPR REAL,
                ECP_PAC INTEGER,
                ECP_PACF INTEGER
            )''')

        # create PA table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PA (
                id TEXT NOT NULL PRIMARY KEY,
                datatype TEXT,
                test_id TEXT,
                ECP_id TEXT,
                time_init TIMESTAMP,
                phase INTEGER,
                ECP_number INTEGER,
                PA_number INTEGER,
                PA_success BOOL,
                PAD REAL,
                PAR REAL,
                P1A REAL,
                P1B REAL,
                P1C REAL,
                P1D REAL,
                P2A REAL,
                P2B REAL,
                P2C REAL,
                P2D REAL,
                kw_angl_x_target REAL,
                kw_angl_y_target REAL,
                kw_dist_x_target REAL,
                kw_dist_y_target REAL,
                kw_dist_struct_A REAL,
                kw_dist_struct_B REAL,
                kw_dist_struct_C REAL,
                kw_dist_struct_D REAL
            )''')

        conn.commit()
    
    
        ### DON'T COMMIT UNTIL ALL INSERTIONS ARE DONE! ###

        # insert TEST_data into database
        cursor.execute('''
            INSERT INTO TEST (
                id,
                datatype,
                PA_ids,
                ECP_ids,
                time_init,
                phase,
                name,
                surname,
                gender,
                age,
                specialization_year,
                num_operations,
                test_duration,
                test_radiation,
                test_PAC,
                test_PACF,
                test_ECPC
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (  TEST_data['id'],
                TEST_data['datatype'],
                ";".join(TEST_data['PA_ids']),
                ";".join(TEST_data['ECP_ids']),
                datetime.fromtimestamp(round(TEST_data["time_init"], 0)),
                TEST_data['phase'],
                TEST_data['name'],
                TEST_data['surname'],
                TEST_data['gender'],
                TEST_data['age'],
                TEST_data['specialization_year'],
                TEST_data['num_operations'],
                TEST_data['test_duration'],
                TEST_data['test_radiation'],
                TEST_data['test_PAC'],
                TEST_data['test_PACF'],
                TEST_data['test_ECPC']))
        
        # insert ECPs into database
        for ECP_data in ECPs:
            cursor.execute('''
                INSERT INTO ECP (
                    id,
                    datatype,
                    test_id,
                    PA_ids,
                    time_init,
                    phase,
                    ECP_number,
                    ECPD,
                    ECPR,
                    ECP_PAC,
                    ECP_PACF
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (  ECP_data['id'],
                    ECP_data['datatype'],
                    ECP_data['test_id'],
                    ";".join(ECP_data['PA_ids']),
                    datetime.fromtimestamp(round(ECP_data["time_init"], 0)),
                    ECP_data['phase'],
                    ECP_data['ECP_number'],
                    ECP_data['ECPD'],
                    ECP_data['ECPR'],
                    ECP_data['ECP_PAC'],
                    ECP_data['ECP_PACF']))

        # insert PAs into database
        for PA_data in PAs:
            cursor.execute('''
                INSERT INTO PA (
                    id,
                    datatype,
                    test_id,
                    ECP_id,
                    time_init,
                    phase,
                    ECP_number,
                    PA_number,
                    PA_success,
                    PAD,
                    PAR,
                    P1A,
                    P1B,
                    P1C,
                    P1D,
                    P2A,
                    P2B,
                    P2C,
                    P2D
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (  PA_data["PA"]["id"],
                    PA_data["PA"]["datatype"],
                    PA_data["PA"]["test_id"],
                    PA_data["PA"]["ECP_id"],
                    datetime.fromtimestamp(round(PA_data["PA"]["time_init"], 0)),
                    PA_data["PA"]["phase"],
                    PA_data["PA"]["ECP_number"],
                    PA_data["PA"]["PA_number"],
                    PA_data["PA"]["PA_success"],
                    PA_data["PA"]["PAD"],
                    PA_data["PA"]["PAR"],
                    PA_data["PA"]["P1A"],
                    PA_data["PA"]["P1B"],
                    PA_data["PA"]["P1C"],
                    PA_data["PA"]["P1D"],
                    PA_data["PA"]["P2A"],
                    PA_data["PA"]["P2B"],
                    PA_data["PA"]["P2C"],
                    PA_data["PA"]["P2D"]))
    except sqlite3.Error as er:
        logger.error(f"-------------------")
        logger.error(f"SQLite traceback  : " + " - ".join([str(x).strip() for x in sys.exc_info()]))
        logger.error(f"SQLite error line : " + str(er.__traceback__.tb_lineno))
        logger.error(f"SQLite error      : " + str(er))
        sys.exit()
        
    conn.commit()
    conn.close()
    logger.info("SAVED ON DATABASE!")
