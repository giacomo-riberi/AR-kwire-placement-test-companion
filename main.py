import sqlite3
import time
from datetime import datetime
import secrets
import sys, traceback
import signal

import utils.utils as utils
from utils import logger

version = "v1.1"

ECPs = []
PAs = []
ci = utils.custom_input()

def main():
    def handler(signum, frame):
        logger.info("\nexiting. DATA NOT SAVED!")
        exit(0)
    signal.signal(signal.SIGINT, handler)

    logger.info(f"# POSITIONING TEST COMPANION ({version}) #\n")

    TEST_data = TEST()

    save_db(TEST_data)

    logger.info("bye!")


def save_db(TEST_data):
    "save_db saves data on database"

    global ECPs, PAs

    try:
        conn = sqlite3.connect(f'positioning_test_data-({version}).db') # Create a connection to the SQLite database (or create it if it doesn't exist)
        cursor = conn.cursor() # Create a cursor object to interact with the database

        # create TEST table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TEST (
                id TEXT NOT NULL PRIMARY KEY,
                datatype TEXT,
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
                test_ECPC INTEGER,
                PA_ids TEXT,
                ECP_ids TEXT
            )''')

        # create ECP table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ECP (
                id TEXT NOT NULL PRIMARY KEY,
                datatype TEXT,
                time_init TIMESTAMP,
                phase INTEGER,
                ECP_number INTEGER,
                ECPD REAL,
                ECPR REAL,
                ECP_PAC INTEGER,
                ECP_PACF INTEGER,
                test_id TEXT,
                PA_ids TEXT
            )''')

        # create PA table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PA (
                id TEXT NOT NULL PRIMARY KEY,
                datatype TEXT,
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
                test_id TEXT,
                ECP_id TEXT
            )''')

        conn.commit()
    
    
        ### DON'T COMMIT UNTIL ALL INSERTIONS ARE DONE! ###

        # insert TEST_data into database
        cursor.execute('''
            INSERT INTO TEST (
                id,
                datatype,
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
                test_ECPC,
                PA_ids,
                ECP_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (  TEST_data['id'],
                TEST_data['datatype'],
                TEST_data['time_init'],
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
                TEST_data['test_ECPC'],
                ",".join(TEST_data['PA_ids']),
                ",".join(TEST_data['ECP_ids'])))
        
        # insert ECPs into database
        for ECP_data in ECPs:
            cursor.execute('''
                INSERT INTO ECP (
                    id,
                    datatype,
                    time_init,
                    phase,
                    ECP_number,
                    ECPD,
                    ECPR,
                    ECP_PAC,
                    ECP_PACF,
                    test_id,
                    PA_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (  ECP_data['id'],
                    ECP_data['datatype'],
                    ECP_data['time_init'],
                    ECP_data['phase'],
                    ECP_data['ECP_number'],
                    ECP_data['ECPD'],
                    ECP_data['ECPR'],
                    ECP_data['ECP_PAC'],
                    ECP_data['ECP_PACF'],
                    ECP_data['test_id'],
                    ",".join(ECP_data['PA_ids'])))

        # insert PAs into database
        for PA_data in PAs:
            cursor.execute('''
                INSERT INTO PA (
                    id,
                    datatype,
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
                    P2D,
                    test_id,
                    ECP_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (  PA_data["id"],
                    PA_data["datatype"],
                    PA_data["time_init"],
                    PA_data["phase"],
                    PA_data["ECP_number"],
                    PA_data["PA_number"],
                    PA_data["PA_success"],
                    PA_data["PAD"],
                    PA_data["PAR"],
                    PA_data["P1A"],
                    PA_data["P1B"],
                    PA_data["P1C"],
                    PA_data["P1D"],
                    PA_data["P2A"],
                    PA_data["P2B"],
                    PA_data["P2C"],
                    PA_data["P2D"],
                    PA_data["test_id"],
                    PA_data["ECP_id"]))
    except sqlite3.Error as er:
        logger.error(f"-------------------")
        logger.error(f"SQLite traceback  : " + " - ".join([str(x).strip() for x in sys.exc_info()]))
        logger.error(f"SQLite error line : " + str(er.__traceback__.tb_lineno))
        logger.error(f"SQLite error      : " + str(er))
        sys.exit()
        
    conn.commit()
    conn.close()
    logger.info("SAVED ON DATABASE!")


def TEST():
    "TEST performs 3 ECPs with multiple PA"

    global ECPs

    logger.info("# BEGIN POSITIONING TEST FOR A CANDIDATE (ONE SINGLE PHASE) #\n")    

    logger.info(f"# {datetime.now().strftime('%Y/%m/%d - %H:%M:%S')} #")

    logger.info("DATA COLLECTION")
    test_data = {
        "id": secrets.token_hex(3),
        "datatype": "test",
        "time_init": datetime.now(),
        "phase":                ci.int(" |-- phase [INTEGER]:               "),
        "name":                 ci.str(" |-- name [STRING]:                 "),
        "surname":              ci.str(" |-- surname [STRING]:              "),
        "gender":               ci.acc(" |-- gender [M/F]:                  ", ["m", "f"]).upper(),
        "age":                  ci.int(" |-- age [INTEGER]:                 "),
        "specialization_year":  ci.int(" |-- specialization year [INTEGER]: "),
        "num_operations":       ci.int(" |-- operations count [INTEGER]:    "),
        "test_duration": 0.0,   # to update
        "test_radiation": 0.0,  # to update
        "test_PAC": 0,          # to update
        "test_PACF": 0,         # to update
        "test_ECPC": 0,         # to update
        "PA_ids": [],           # to update
        "ECP_ids": []           # to update
    }

    for ECP_number in range(1, 4):
        ECP_data = ECP(test_data["phase"], test_data["id"], ECP_number)

        # add ECP_data to ECPs
        ECPs.append(ECP_data)

        # update test_data
        test_data["test_duration"]  += ECP_data["ECPD"]
        test_data["test_radiation"] += ECP_data["ECPR"]
        test_data["test_PAC"]       += ECP_data["ECP_PAC"]
        test_data["test_PACF"]      += ECP_data["ECP_PACF"]
        test_data["test_ECPC"]       = ECP_number
        test_data["PA_ids"].extend(ECP_data["PA_ids"])
        test_data["ECP_ids"].append(ECP_data["id"])

    return test_data

def ECP(phase, test_id, ECP_number):
    "ECP performs single ECP with multiple PA"

    global PAs

    ECP_data = {
        "id": secrets.token_hex(4),
        "datatype": "ecp",
        "time_init": datetime.now(),
        "phase": phase,
        "ECP_number": ECP_number,
        "ECPD": 0.0,        # to update
        "ECPR": 0.0,        # to update
        "ECP_PAC": 0,       # to update
        "ECP_PACF": 0,      # to update
        "test_id": test_id,
        "PA_ids": []        # to update
    }

    PA_number = 1
    while True:
        PA_data = PA(phase, test_id, ECP_number, ECP_data["id"], PA_number)

        # add PA_data to PAs
        PAs.append(PA_data)

        # update ECP_data
        ECP_data["ECPD"] += PA_data["PAD"]
        ECP_data["ECPR"] += PA_data["PAR"]
        ECP_data["ECP_PAC"] = PA_number
        ECP_data["ECP_PACF"] += 0 if PA_data["PA_success"] else 1
        ECP_data["PA_ids"].append(PA_data["id"])
        
        if PA_data["PA_success"]:
            break
        PA_number += 1
    
    return ECP_data
    
    
def PA(phase, test_id, ECP_number, ECP_id, PA_number):
    "PA performs single PA"

    def terminatePA(PA_success: bool):
        "terminatePA terminates PA, performs data extraction and candidate extracts K-wire"

        chrono.pause() # pause chronometer to get data
        logger.info(f"DATA COLLECTION - PA{ECP_number}.{PA_number}")
        PA_data = {
            "id": secrets.token_hex(5),
            "datatype": "pa",
            "time_init": time_init,
            "phase": phase,
            "ECP_number": ECP_number,
            "PA_number": PA_number,
            "PA_success": PA_success,
            # "PAD", # set after K-wire extraction
            "PAR": ci.flo(" |-- positioning attempt RADIATION [FLOAT]: "),
            "P1A": ci.flo(" |-- P1A [FLOAT]: "),
            "P1B": ci.flo(" |-- P1B [FLOAT]: "),
            "P1C": ci.flo(" |-- P1C [FLOAT]: "),
            "P1D": ci.flo(" |-- P1D [FLOAT]: "),
            "P2A": ci.flo(" |-- P2A [FLOAT]: "),
            "P2B": ci.flo(" |-- P2B [FLOAT]: "),
            "P2C": ci.flo(" |-- P2C [FLOAT]: "),
            "P2D": ci.flo(" |-- P2D [FLOAT]: "),
            "test_id": test_id,
            "ECP_id": ECP_id
        }
        chrono.start() # start chronometer to include also extraction time in PA

        ci.all("CANDIDATE: extract the K-wire [ENTER when done]: ")
        PA_data["PAD"] = chrono.reset()
        return PA_data

    logger.info(f"\n------------------------\nPA{ECP_number}.{PA_number} START!")
    ci.all("PERFORM:\t reset x-ray machine [ENTER when done]: ")
    
    chrono = utils.chronometer()
    time_init = datetime.fromtimestamp(chrono.start())

    i = ci.acc("CANDIDATE:\t insert K-wire, checks it and declares it failed[f] or successful[s]: ", ["f", "s"])
    if i.lower() == 'f': # PA FAILED
        logger.info("\t\t |-candidate has FAILED positioning attempt!")
        return terminatePA(False)
    elif i.lower() == 's': # PA SUCCESS
        logger.info("\t\t |-candidate has performed SUCCESSFUL positioning attempt!")
        return terminatePA(True)
    
if __name__ == "__main__":
    main()